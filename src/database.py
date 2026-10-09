import sqlite3

DB_PATH = "applications.db"


def get_connection():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    con = get_connection()
    con.execute(
        "CREATE TABLE IF NOT EXISTS applications (id INTEGER PRIMARY KEY, company TEXT, role TEXT, status TEXT, applied_date DATE, notes TEXT DEFAULT '')"
    )
    con.commit()
    con.close()
