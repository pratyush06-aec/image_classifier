import sqlite3

def init_db():
    conn = sqlite3.connect("classifier.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT,
        prediction TEXT
    )
    """)

    conn.commit()
    conn.close()