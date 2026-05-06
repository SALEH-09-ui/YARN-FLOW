import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "yarnflow.db")

if not os.path.exists(DB):
    print("❌ Database file not found:", DB)
    exit(1)

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def print_table(title, query):
    print(f"\n--- {title} ---")
    try:
        rows = cur.execute(query).fetchall()
        if not rows:
            print("(empty)")
            return
        for r in rows:
            print(dict(r))
    except Exception as e:
        print("ERROR:", e)

print_table("USERS", "SELECT * FROM users")
print_table("PRODUCTS", "SELECT * FROM products")
print_table("TRANSACTIONS", "SELECT * FROM transactions")
print_table("MESSAGES", "SELECT * FROM messages")

conn.close()
