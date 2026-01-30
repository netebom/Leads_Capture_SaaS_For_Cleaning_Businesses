CREATE TABLE IF NOT EXISTS pages (
    page_id TEXT PRIMARY KEY,
    page_name TEXT,
    page_token TEXT,
    owner_email TEXT,
    dashboard_token TEXT UNIQUE,
    created_at TEXT,
    is_paid INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS conversations (
    sender_id TEXT,
    page_id TEXT,
    step INTEGER,
    cleaning_type TEXT,
    city TEXT,
    phone_number TEXT,
    PRIMARY KEY(sender_id, page_id)
);

CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_id TEXT,
    cleaning_type TEXT,
    city TEXT,
    phone_number TEXT,
    timestamp TEXT
);

CREATE TABLE IF NOT EXISTS customers (
    page_id TEXT PRIMARY KEY,
    owner_email TEXT,
    dashboard_token TEXT UNIQUE,
    is_paid INTEGER DEFAULT 0
);

