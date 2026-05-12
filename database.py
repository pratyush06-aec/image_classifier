import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    """Creates a new psycopg2 connection to Supabase using env vars."""
    # try:
    #     conn = get_connection()
    #     print("✅ Connected to Supabase")
    #     conn.close()
    # except Exception as e:
    #     print("❌ Connection error:", e)
    return psycopg2.connect(
        DATABASE_URL,
        sslmode='require',
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

def init_supabase_db():
    """Ensures the predictions table exists in Supabase with the correct schema."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Create the table if it doesn't exist at all
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id SERIAL PRIMARY KEY,
                filename TEXT NOT NULL,
                prediction TEXT NOT NULL,
                confidence REAL NOT NULL
            )
        """)

        # If the table already existed but is missing columns, add them.
        # Each ALTER is wrapped individually so one failure doesn't block the others.
        for col_name, col_type in [("filename", "TEXT"), ("prediction", "TEXT"), ("confidence", "REAL")]:
            try:
                cursor.execute(f"ALTER TABLE predictions ADD COLUMN {col_name} {col_type}")
            except psycopg2.errors.DuplicateColumn:
                conn.rollback()  # Reset transaction after the expected error

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Supabase predictions table verified/created.")
    except Exception as e:
        print(f"⚠️ Could not initialize Supabase table: {e}")

# Auto-initialize the table on module import
init_supabase_db()

def insert_prediction(filename, prediction, confidence):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO predictions (filename, prediction, confidence) VALUES (%s, %s, %s)",
        (filename, prediction, confidence)
    )

    conn.commit()
    cursor.close()
    conn.close()

def fetch_history():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions ORDER BY id ASC")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data