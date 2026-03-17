# ==========================================================
# FINAL DATABASE MODULE (AUTO-UPGRADE SAFE + DUPLICATE PROOF)
# Supports:
# - Fraud detection
# - Anomaly detection
# - Risk scoring
# - Chat history
# - Voice history
# - Multilingual chatbot
# - Email authentication
# - Phone OTP authentication
# - User management
# - Device-based authentication
# - Transaction Intelligence
# - Deduction Transparency Engine
# - UNIQUE Constraint for Transactions (Enterprise Fix)
# Production-grade
# ==========================================================

import sqlite3

DB_NAME = "transactions.db"


# ==========================================================
# INTERNAL HELPER: CHECK COLUMN EXISTS
# ==========================================================

def column_exists(conn, table, column):
    cursor = conn.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cursor.fetchall()]
    return column in columns


# ==========================================================
# INTERNAL HELPER: ADD COLUMN SAFELY
# ==========================================================

def add_column_if_missing(conn, table, column, col_type):
    if not column_exists(conn, table, column):
        conn.execute(
            f"ALTER TABLE {table} ADD COLUMN {column} {col_type}"
        )


# ==========================================================
# INIT DATABASE (AUTO MIGRATION SAFE)
# ==========================================================

def init_db():

    conn = sqlite3.connect(DB_NAME)

    # ======================================================
    # USERS TABLE
    # ======================================================

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password_hash TEXT,
        email_verified INTEGER DEFAULT 0,
        phone TEXT UNIQUE,
        phone_verified INTEGER DEFAULT 0,
        auth_method TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ======================================================
    # USER DEVICES TABLE
    # ======================================================

    conn.execute("""
    CREATE TABLE IF NOT EXISTS user_devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        device_id TEXT,
        device_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, device_id)
    )
    """)

    # ======================================================
    # TRANSACTIONS TABLE (DUPLICATE PROOF)
    # ======================================================

    conn.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        description TEXT,
        amount REAL,
        type TEXT,
        category TEXT,
        mode TEXT,
        bank TEXT,
        product_amount REAL,
        deducted_amount REAL,
        extra_charge REAL,
        charge_reason TEXT,
        fraud INTEGER DEFAULT 0,
        anomaly INTEGER DEFAULT 0,
        risk_score REAL DEFAULT 0,
        confidence REAL DEFAULT 0,
        user_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, date, description, amount)
    )
    """)

    # Auto-upgrade safety
    add_column_if_missing(conn, "transactions", "category", "TEXT")
    add_column_if_missing(conn, "transactions", "mode", "TEXT")
    add_column_if_missing(conn, "transactions", "bank", "TEXT")
    add_column_if_missing(conn, "transactions", "product_amount", "REAL")
    add_column_if_missing(conn, "transactions", "deducted_amount", "REAL")
    add_column_if_missing(conn, "transactions", "extra_charge", "REAL")
    add_column_if_missing(conn, "transactions", "charge_reason", "TEXT")
    add_column_if_missing(conn, "transactions", "fraud", "INTEGER DEFAULT 0")
    add_column_if_missing(conn, "transactions", "anomaly", "INTEGER DEFAULT 0")
    add_column_if_missing(conn, "transactions", "risk_score", "REAL DEFAULT 0")
    add_column_if_missing(conn, "transactions", "confidence", "REAL DEFAULT 0")
    add_column_if_missing(conn, "transactions", "user_id", "INTEGER")

    # ======================================================
    # CHAT HISTORY TABLE
    # ======================================================

    conn.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT,
        language TEXT,
        user_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    add_column_if_missing(conn, "chat_history", "user_id", "INTEGER")

    # ======================================================
    # RISK HISTORY TABLE
    # ======================================================

    conn.execute("""
    CREATE TABLE IF NOT EXISTS risk_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        risk_score REAL,
        user_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    add_column_if_missing(conn, "risk_history", "user_id", "INTEGER")

    # ======================================================
    # VOICE HISTORY TABLE
    # ======================================================

    conn.execute("""
    CREATE TABLE IF NOT EXISTS voice_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transcript TEXT,
        user_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    add_column_if_missing(conn, "voice_history", "user_id", "INTEGER")

    conn.commit()
    conn.close()


# ==========================================================
# CREATE USER
# ==========================================================

def create_user(email=None, password_hash=None, phone=None, auth_method=None):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        INSERT INTO users
        (email, password_hash, phone, auth_method)
        VALUES (?, ?, ?, ?)
    """, (email, password_hash, phone, auth_method))

    conn.commit()
    conn.close()


# ==========================================================
# GET USER BY EMAIL
# ==========================================================

def get_user_by_email(email):

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    user = conn.execute("""
        SELECT * FROM users WHERE email=?
    """, (email,)).fetchone()

    conn.close()

    return dict(user) if user else None


# ==========================================================
# GET USER BY PHONE
# ==========================================================

def get_user_by_phone(phone):

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    user = conn.execute("""
        SELECT * FROM users WHERE phone=?
    """, (phone,)).fetchone()

    conn.close()

    return dict(user) if user else None


# ==========================================================
# VERIFY EMAIL
# ==========================================================

def verify_email(email):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        UPDATE users
        SET email_verified=1
        WHERE email=?
    """, (email,))

    conn.commit()
    conn.close()


# ==========================================================
# VERIFY PHONE
# ==========================================================

def verify_phone(phone):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        UPDATE users
        SET phone_verified=1
        WHERE phone=?
    """, (phone,))

    conn.commit()
    conn.close()


# ==========================================================
# SAVE USER DEVICE
# ==========================================================

def save_user_device(user_id, device_id, device_name):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        INSERT OR IGNORE INTO user_devices
        (user_id, device_id, device_name)
        VALUES (?, ?, ?)
    """, (user_id, device_id, device_name))

    conn.commit()
    conn.close()


# ==========================================================
# CHECK IF DEVICE IS KNOWN
# ==========================================================

def is_known_device(user_id, device_id):

    conn = sqlite3.connect(DB_NAME)

    result = conn.execute("""
        SELECT id FROM user_devices
        WHERE user_id=? AND device_id=?
    """, (user_id, device_id)).fetchone()

    conn.close()

    return result is not None


# ==========================================================
# GET USER DEVICES
# ==========================================================

def get_user_devices(user_id):

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT * FROM user_devices
        WHERE user_id=?
    """, (user_id,)).fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ==========================================================
# INSERT TRANSACTION (DUPLICATE SAFE)
# ==========================================================

def insert_transaction(tx, user_id=None):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    INSERT OR IGNORE INTO transactions
    (
        date,
        description,
        amount,
        type,
        category,
        mode,
        bank,
        product_amount,
        deducted_amount,
        extra_charge,
        charge_reason,
        fraud,
        anomaly,
        risk_score,
        confidence,
        user_id
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        tx.get("date"),
        tx.get("description"),
        tx.get("amount"),
        tx.get("type"),
        tx.get("category"),
        tx.get("mode"),
        tx.get("bank"),
        tx.get("product_amount"),
        tx.get("deducted_amount"),
        tx.get("extra_charge"),
        tx.get("charge_reason"),
        int(tx.get("fraud", False)),
        int(tx.get("anomaly", False)),
        float(tx.get("risk_score", 0)),
        float(tx.get("confidence", 0)),
        user_id

    ))

    conn.commit()
    conn.close()


# ==========================================================
# GET ALL TRANSACTIONS
# ==========================================================

def get_all_transactions(user_id=None):

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    if user_id:
        rows = conn.execute("""
            SELECT * FROM transactions
            WHERE user_id=?
            ORDER BY date DESC
        """, (user_id,)).fetchall()
    else:
        rows = conn.execute("""
            SELECT * FROM transactions
            ORDER BY date DESC
        """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ==========================================================
# SAVE CHAT HISTORY
# ==========================================================

def save_chat(question, answer, language, user_id=None):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    INSERT INTO chat_history
    (question, answer, language, user_id)
    VALUES (?, ?, ?, ?)
    """, (question, answer, language, user_id))

    conn.commit()
    conn.close()


# ==========================================================
# SAVE RISK SCORE
# ==========================================================

def save_risk_score(score, user_id=None):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        INSERT INTO risk_history
        (risk_score, user_id)
        VALUES (?, ?)
    """, (score, user_id))

    conn.commit()
    conn.close()


# ==========================================================
# SAVE VOICE TRANSCRIPT
# ==========================================================

def save_voice(transcript, user_id=None):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        INSERT INTO voice_history
        (transcript, user_id)
        VALUES (?, ?)
    """, (transcript, user_id))

    conn.commit()
    conn.close()

# ==========================================================
# DELETE TRANSACTION (Enterprise Safe)
# ==========================================================

def delete_transaction(transaction_id, user_id):

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        DELETE FROM transactions
        WHERE id=? AND user_id=?
    """, (transaction_id, user_id))

    conn.commit()
    conn.close()    

# ==========================================================
# CLEAR USER TRANSACTIONS (SAFE RESET)
# ==========================================================

def clear_user_transactions(user_id):
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        DELETE FROM transactions
        WHERE user_id=?
    """, (user_id,))
    conn.commit()
    conn.close()    