import sqlite3

def init_db():
    """Initializes the database and creates the alerts table if it doesn't exist."""
    conn = sqlite3.connect('alerts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            domain TEXT NOT NULL,
            similar_to TEXT NOT NULL,
            similarity_score INTEGER NOT NULL,
            creation_date TEXT,
            status TEXT NOT NULL,
            keywords_found TEXT,
            screenshot_path TEXT,
            gsb_status TEXT 
        )
    ''')
    conn.commit()
    conn.close()

def add_alert(domain, similar_to, score, creation_date, status, keywords, screenshot_path, gsb_status):
    """Adds a new phishing alert to the database."""
    conn = sqlite3.connect('alerts.db')
    cursor = conn.cursor()
    # Convert list of keywords to a comma-separated string for storage
    keywords_str = ", ".join(keywords) if keywords else ""
    cursor.execute(
        "INSERT INTO alerts (domain, similar_to, similarity_score, creation_date, status, keywords_found, screenshot_path, gsb_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (domain, similar_to, score, creation_date, status, keywords_str, screenshot_path, gsb_status)
    )
    conn.commit()
    conn.close()

def get_all_alerts():
    """Retrieves all alerts from the database, newest first."""
    conn = sqlite3.connect('alerts.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts ORDER BY timestamp DESC")
    alerts = cursor.fetchall()
    conn.close()
    return alerts