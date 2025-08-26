# SQLite veritabanı bağlantısı
import sqlite3
from models import LogCreate, News
from datetime import datetime

DB_PATH = "atlas-trader.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS Logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        level TEXT,
        message TEXT
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS CryptoNews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        url TEXT,
        sentiment TEXT,
        published_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_log(log: LogCreate):
    conn = get_db()
    c = conn.cursor()
    ts = datetime.utcnow().isoformat()
    c.execute("INSERT INTO Logs (timestamp, level, message) VALUES (?, ?, ?)", (ts, log.level, log.message))
    conn.commit()
    log_id = c.lastrowid
    conn.close()
    return log_id

def get_logs():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM Logs ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_log_by_id(log_id: int):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM Logs WHERE id=?", (log_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def add_news(news_list):
    conn = get_db()
    c = conn.cursor()
    for news in news_list:
        c.execute("INSERT INTO CryptoNews (title, url, sentiment, published_at) VALUES (?, ?, ?, ?)",
                  (news["title"], news["url"], news.get("sentiment"), news["published_at"]))
    conn.commit()
    conn.close()

def get_stored_news():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM CryptoNews ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]
