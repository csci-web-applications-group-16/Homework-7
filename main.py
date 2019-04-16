import json
import os
import sqlite3

from flask import Flask, render_template

# get current app directory
basedir = os.path.abspath(os.path.dirname(__file__))

# create a Flask instance
app = Flask(__name__)


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

    return render_template('view-parties.html', parties=results, parties_json=json.dumps(results))


if __name__ == '__main__':
    app.debug = True
    ip = '127.0.0.1'
    app.run(host=ip)
