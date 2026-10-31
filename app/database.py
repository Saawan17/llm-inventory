import sqlite3
from pathlib import Path

# Get the app directory
BASE_DIR = Path(__file__).resolve().parent


# Database file location
DB_PATH = BASE_DIR / "tasks.db"

def get_db_connection():
    """Create a connection to the SQLite database."""
    connection = sqlite3.connect(DB_PATH)
    return connection
    # conn = sqlite3.connect(DB_PATH)
    # conn.row_factory = sqlite3.Row  # Enable dictionary-like access to rows
    # return conn


def initialize_database():
    """Initialize the database and create the tasks table if it doesn't exist."""
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            due_date TEXT,
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()

    cursor.execute("PRAGMA table_info(tasks)")

    columns = cursor.fetchall()

    for column in columns:
        print(column)

    connection.close()

    print("Database initialized and tasks table created (if it didn't exist).")

if __name__ == "__main__":
    initialize_database()




