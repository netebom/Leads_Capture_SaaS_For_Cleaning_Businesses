import sqlite3
import uuid
from datetime import datetime
import os

DB_PATH = os.path.join(os.getcwd(), "database.db")


# -------------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------------------------------
# INITIALIZE DATABASE
# -------------------------------------------------
def init_db():
    conn = get_db()
    cur = conn.cursor()

    # Businesses table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS businesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            country TEXT NOT NULL,
            token TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Leads table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_token TEXT NOT NULL,
            cleaning_type TEXT,
            city TEXT,
            phone TEXT,
            status TEXT DEFAULT 'New',
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# -------------------------------------------------
# BUSINESS LOGIC
# -------------------------------------------------
def create_business(name, email, country):
    token = uuid.uuid4().hex[:8]
    created_at = datetime.utcnow().isoformat()

    conn = get_db()
    conn.execute("""
        INSERT INTO businesses (name, email, country, token, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, country, token, created_at))

    conn.commit()
    conn.close()
    return token


def get_business_by_token(token):
    conn = get_db()
    cur = conn.execute(
        "SELECT * FROM businesses WHERE token = ?",
        (token,)
    )
    business = cur.fetchone()
    conn.close()
    return business


# -------------------------------------------------
# LEADS LOGIC
# -------------------------------------------------
def save_lead(business_token, cleaning_type, city, phone):
    created_at = datetime.utcnow().isoformat()

    conn = get_db()
    cur = conn.execute("""
        INSERT INTO leads (
            business_token,
            cleaning_type,
            city,
            phone,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, 'New', ?)
    """, (business_token, cleaning_type, city, phone, created_at))

    conn.commit()

    lead_id = cur.lastrowid
    cur = conn.execute(
        "SELECT * FROM leads WHERE id = ?",
        (lead_id,)
    )
    lead = cur.fetchone()
    conn.close()

    return lead


def get_leads(business_token):
    conn = get_db()
    cur = conn.execute("""
        SELECT * FROM leads
        WHERE business_token = ?
        ORDER BY id DESC
    """, (business_token,))
    rows = cur.fetchall()
    conn.close()
    return rows


def update_lead_status(lead_id, status):
    conn = get_db()
    conn.execute(
        "UPDATE leads SET status = ? WHERE id = ?",
        (status, lead_id)
    )
    conn.commit()
    conn.close()


def get_leads_for_csv(business_token):
    conn = get_db()
    cur = conn.execute("""
        SELECT cleaning_type, city, phone, status, created_at
        FROM leads
        WHERE business_token = ?
        ORDER BY id DESC
    """, (business_token,))
    rows = cur.fetchall()
    conn.close()
    return rows
