import sqlite3

#Creates party_planner.db
conn = sqlite3.connect('party_planner.db')

c = conn.cursor()

c.execute("""CREATE TABLE places(
            start_time integer,
            end_time integer,
            location string,

            PRIMARY KEY(start_time, end_time)
)""")

#Data
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


#c.execute("SELECT * FROM places WHERE location = 'lounge'")

#print(c.fetchall())


conn.commit()

conn.close()
