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

    c = conn.cursor()

    c.execute("""CREATE TABLE places(
                    start_time integer,
                    end_time integer,
                    location string,

                    PRIMARY KEY(start_time, end_time)
        )""")

    # Data
    c.execute("INSERT INTO places VALUES (19,22,'LOUNGE')")
    c.execute("INSERT INTO places VALUES (18,24,'HOOKAH LOT')")
    c.execute("INSERT INTO places VALUES (20,2,'PONTANA BOBS')")
    c.execute("INSERT INTO places VALUES (21,3,'HIGH LIFE')")
    c.execute("INSERT INTO places VALUES (8,22,'ZACS HOUSE')")
    c.execute("INSERT INTO places VALUES (5,22,'NAVIDS HOUSE')")
    c.execute("INSERT INTO places VALUES (16,2,'JESSICAS HOUSE')")
    c.execute("INSERT INTO places VALUES (20,3,'7TH ON 7TH')")
    c.execute("INSERT INTO places VALUES (9,4,'SUP DOGS')")
    c.execute("INSERT INTO places VALUES (8,8,'WAFFLE HOUSE')")
    c.execute("INSERT INTO places VALUES (12,2,'DIAMOND GIRLS')")

    # c.execute("SELECT * FROM places WHERE location = 'lounge'")

    # print(c.fetchall())

    conn.commit()

    conn.close()

    return render_template('view-parties.html')


if __name__ == '__main__':
    app.debug = True
    ip = '127.0.0.1'
    app.run(host=ip)
