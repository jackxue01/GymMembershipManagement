import sqlite3

def get_connection():
    return sqlite3.connect("gym.db")

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        phone TEXT,
        plan_id INTEGER,
        start_date DATE NOT NULL,
        end_date DATE,
        is_active BOOLEAN
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plans (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      type TEXT NOT NULL,
      duration_months INTEGER NOT NULL,
      price REAL NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS checkins (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      FOREIGN KEY (member_id) REFERENCES members(id) NOT NULL,
      checkin_time DATETIME NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      FOREIGN KEY (member_id) REFERENCES members(id) NOT NULL,
      date_paid DATE NOT NULL,
      amount REAL NOT NULL,
      plan_id INTEGER NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      date DATETIME NOT NULL,
      type TEXT NOT NULL,
      FOREIGN KEY (member_id) REFERENCES members(id)
    )
    """)

    conn.commit()
    conn.close()