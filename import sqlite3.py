import sqlite3

conn = sqlite3.connect("tickets.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL
)
""")
conn.commit()
conn.close()

def log_ticket(message):
    conn = sqlite3.connect("tickets.db")
    c = conn.cursor()
    c.execute("INSERT INTO tickets (description) VALUES (?)", (message,))
    conn.commit()
    conn.close()
