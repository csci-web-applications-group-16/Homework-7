import os
import sqlite3

import pandas
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename

import util
import sqlite3

# Import -- Example 42
# get current app directory
basedir = os.path.abspath(os.path.dirname(__file__))

# create a Flask instance
app = Flask(__name__)


def database_execute(query, args=()):
    try:
        # Creates party_planner.db
        conn = sqlite3.connect('party_planner.db')

        c = conn.cursor()
        c.execute(query, args)

        conn.commit()
    except:
        conn.rollback()
        return False
    finally:
        conn.close()
        return True


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
    return render_template('remove-party.html')


@app.route('/view-parties.html')
def view_parties():
    conn = sqlite3.connect('party_planner.db')
    cursor = conn.cursor()
    cursor.execute("SELECT party_name, location_map_query FROM parties")
    results = cursor.fetchall()
    conn.close()

    return render_template('view-parties.html', parties=results)


@app.route('/api/get-parties', methods=['GET'])
def get_parties():
    query = "SELECT * FROM parties"
    query_res = database_fetch(query)
    if(query_res == None):
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
    add_query = 'INSERT INTO parties (start_time, end_time, party_name, user_id, location_map_query) VALUES(?,?,?,?,?)'
    query_params = (form['start_time'], form['end_time'], form[
                    'party_name'], form['user_id'], form['location_map_query'])
    if(database_execute(add_query, query_params)):
        return jsonify({'status': 201})
    else:
        return jsonify({'status': 304})


if __name__ == '__main__':
    app.debug = True
    ip = '127.0.0.1'
    app.run(host=ip)
