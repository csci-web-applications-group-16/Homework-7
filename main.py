import os
import sqlite3

from flask import Flask, request, render_template, jsonify

basedir = os.path.abspath(os.path.dirname(__file__))

# create a Flask instance
app = Flask(__name__)


def database_execute(query, args=()):
    ret = True
    try:
        # Creates party_planner.db
        conn = sqlite3.connect('party_planner.db')

        c = conn.cursor()
        c.execute(query, args)

        conn.commit()
    except:
        conn.rollback()
        ret = False
    finally:
        conn.close()

        return ret


def database_insert(query, args=()):
    try:
        # Creates party_planner.db
        conn = sqlite3.connect('party_planner.db')

        c = conn.cursor()
        c.execute(query, args)
        ret = c.lastrowid
        conn.commit()
    except:
        conn.rollback()
        ret = None
    finally:
        conn.close()

        return ret


def database_fetch(query, args=()):
    try:
        conn = sqlite3.connect('party_planner.db')
        c = conn.execute(query, args)
        ret = c.fetchall()
    except:
        conn.rollback()
        ret = None
    finally:
        conn.close()
        return ret


# From Example 42 -->
# Original Code Snippit Commented Out
# app.config['DATA_FILE'] = UPLOAD_FOLDER + 'NRDC_data.csv'


@app.route('/', methods=['GET'])
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/add-party.html')
def add_party():
    return render_template('add-party.html')


@app.route('/edit-party.html')
def edit_party():
    return render_template('edit-party.html')


@app.route('/remove-party.html')
def remove_party():
    party_id_arg = request.args.get('party-id')

    if party_id_arg is not None:
        results = database_fetch(
            "SELECT party_id, party_name, location_map_query FROM parties WHERE party_id='" +
            party_id_arg + "'"
        )
    else:
        results = database_fetch(
            "SELECT party_id, party_name, location_map_query FROM parties")
        party_id_arg = -1

    return render_template('remove-party.html', party_id=party_id_arg, parties=results)


@app.route('/view-parties.html')
def view_parties():
    party_id_arg = request.args.get('party-id')

    if party_id_arg is not None:
        results = database_fetch(
            "SELECT party_id, party_name, location_map_query FROM parties WHERE party_id='" +
            party_id_arg + "'"
        )
    else:
        results = database_fetch(
            "SELECT party_id, party_name, location_map_query FROM parties")
        party_id_arg = -1

    return render_template('view-parties.html', party_id=party_id_arg, parties=results)


@app.route('/api/get-parties', methods=['GET'])
def get_parties():
    query = "SELECT * FROM parties"
    query_res = database_fetch(query)
    if query_res is None:
        return jsonify({'status': 401})

    ret = []
    rows = ['party_id', 'start_time', 'end_time',
            'party_name', 'location_map_query']
    for v in query_res:
        ret.append({row: v[i] for i, row in enumerate(rows)})

    return jsonify({'parties': ret, 'status': 201})


@app.route('/api/get-party/<int:party_id>', methods=['GET'])
def get_party(party_id):
    query = 'SELECT * FROM parties WHERE party_id=?'
    query_res = database_fetch(query, (party_id,))

    if query_res == None:
        return jsonify({'status': 401})

    ret = []
    rows = ['party_id', 'start_time', 'end_time',
            'party_name', 'user_id', 'location_map_query']
    for v in query_res:
        ret.append({row: v[i] for i, row in enumerate(rows)})

    return jsonify({'parties': ret, 'status': 201})


@app.route('/api/add-party', methods=['POST'])
def insert_party():
    form = request.form
    if(form['start_time'] == '' or form['end_time'] == '' or form['party_name'] == '' or form['location_map_query'] == ''):
        return jsonify({'status': 401})

    add_query = 'INSERT INTO parties (start_time, end_time, party_name, location_map_query) VALUES(?,?,?,?)'
    query_params = (form['start_time'], form['end_time'], form[
        'party_name'], form['location_map_query'])

    party_id = database_insert(add_query, query_params)
    if(party_id != None):
        return jsonify({'status': 201, 'party_id': party_id})
    else:
        return jsonify({'status': 401})


@app.route('/api/remove-party', methods=['POST'])
def remove_party_api():
    form = request.form
    remove_query = 'DELETE FROM parties WHERE party_id=?'
    if 'party_id' in form and database_execute(remove_query, (form['party_id'],)):
        return jsonify({'status': 200})
    else:
        return jsonify({'status': 401})


if __name__ == '__main__':
    app.debug = True
    ip = '127.0.0.1'
    app.run(host=ip)
