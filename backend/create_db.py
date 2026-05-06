import sqlite3
import os

# ---------------- DB PATH ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "yarnflow.db")

# ---------------- CONNECT ----------------
conn = sqlite3.connect(DB)
cur = conn.cursor()

# ---------------- SAFETY ----------------
cur.execute("PRAGMA foreign_keys = ON")

# ---------------- USERS ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    mobile TEXT UNIQUE NOT NULL,
    nid TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# ---------------- PRODUCTS ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    stock INTEGER NOT NULL CHECK(stock >= 0),
    price INTEGER NOT NULL CHECK(price >= 0)
)
""")

# ---------------- TRANSACTIONS ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    product TEXT NOT NULL,
    qty INTEGER NOT NULL CHECK(qty > 0),
    paid INTEGER NOT NULL CHECK(paid >= 0),
    due INTEGER NOT NULL CHECK(due >= 0),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
""")

# ---------------- MESSAGES ----------------
cur.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    reply TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
""")

# ---------------- DEFAULT PRODUCTS ----------------
cur.execute("SELECT COUNT(*) FROM products")
count = cur.fetchone()[0]

if count == 0:
    cur.executemany("""
        INSERT INTO products (name, stock, price)
        VALUES (?, ?, ?)
    """, [
        ("16/1 Doublepan", 526, 5000),
        ("42/1 Promax", 820, 6585),
        ("42/1 Ambia", 430, 7632),
        ("50/1 Promax M", 790, 3500),
        ("40/1 Makson", 990, 4557),
        ("80/1 Taqrim", 2270, 5500),
        ("54/1 Moltazim", 2780, 6003)
    ])

# ---------------- COMMIT & CLOSE ----------------
conn.commit()
conn.close()

print("✅ Database created successfully.")
