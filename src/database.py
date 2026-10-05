import sqlite3
from enum import Enum

DB_PATH = "applications.db"

class Status(str, Enum):
    INTERVIEW_DONE = "interview_done"
    APPLIED = "applied"
    WAITING = "waiting"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    OFFER = "offer"
    REJECTED = "rejected"
    ACCEPTED = "accepted"

def get_connection():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = get_connection()
    con.execute("CREATE TABLE IF NOT EXISTS applications (id INTEGER PRIMARY KEY, company TEXT, role TEXT, status TEXT, applied_date DATE, notes TEXT)")
    con.commit()
    con.close()

