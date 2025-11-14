import sqlite3
from datetime import datetime

DB_FILE = "deployments.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS deployments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT,
            url TEXT,
            qa_result TEXT,
            status TEXT,
            created_at DATETIME
        )
    """)
    conn.commit()
    conn.close()

def save_deployment(project_name, url, qa_result, status="deploying"):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO deployments (project_name, url, qa_result, status, created_at) VALUES (?, ?, ?, ?, ?)",
              (project_name, url, qa_result, status, datetime.now()))
    conn.commit()
    conn.close()

def update_deployment_status(url, status, qa_result=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if qa_result:
        c.execute("UPDATE deployments SET status=?, qa_result=? WHERE url=?", (status, qa_result, url))
    else:
        c.execute("UPDATE deployments SET status=? WHERE url=?", (status, url))
    conn.commit()
    conn.close()

def get_deployments():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM deployments ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return rows
