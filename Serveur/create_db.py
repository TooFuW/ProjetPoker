from sqlite3 import *

sql_conn = connect("userdata.db")
cur = sql_conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS userdata(
            id INTEGER PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
)
""")