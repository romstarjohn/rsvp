import sqlite3

conn = sqlite3.connect("rsvp.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE rsvp (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    participation TEXT,
    relation TEXT,
    message TEXT,
    created_at TEXT
)
""")

conn.commit()
conn.close()
print("Database created")
