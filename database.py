import sqlite3
import os
from datetime import datetime

# Database file location in the same directory
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')

# Allowed response options for validation
ALLOWED_RESPONSES = [
    "Maybe We Can Try Again ♡",
    "I Need More Time",
    "I'm Willing to Try ♡",
    "I Need Some Time"
]

def get_connection():
    """Create and return a database connection with dictionary-like row access."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the SQLite database and create the responses table if it doesn't exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                choice TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()

def save_response(choice):
    """
    Validate and save the user's apology response with the current timestamp.
    Returns True if valid and saved, False otherwise.
    """
    if choice not in ALLOWED_RESPONSES:
        return False
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO responses (choice, timestamp) VALUES (?, ?)',
            (choice, current_time)
        )
        conn.commit()
    return True

def get_latest_response():
    """Retrieve the most recent saved response, or None if no responses exist yet."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM responses ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

def get_all_responses():
    """Retrieve all saved responses ordered by newest first."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM responses ORDER BY id DESC')
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

# Initialize database when this module is imported or run
if __name__ == '__main__':
    init_db()
    print("Database initialized successfully at:", DB_FILE)
