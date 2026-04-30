import sqlite3

DB_PATH= "instance/classifier.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
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