import sqlite3
import os

# ================= DATABASE PATH =================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB = os.path.join(BASE_DIR, "yarnflow.db")

# ================= CHECK DB EXISTS =================

if not os.path.exists(DB):

    print("DATABASE NOT FOUND")

    exit()

# ================= CONNECT DATABASE =================

conn = sqlite3.connect(DB)

conn.row_factory = sqlite3.Row

cur = conn.cursor()

# ================= PRINT FUNCTION =================

def print_table(title, query):

    print("\n==============================")
    print(title)
    print("==============================")

    try:

        rows = cur.execute(query).fetchall()

        if not rows:

            print("NO DATA")

            return

        for r in rows:

            print(dict(r))

    except Exception as e:

        print("ERROR :", e)

# ================= SHOW ALL TABLES =================

print_table(
    "USERS TABLE",
    "SELECT * FROM users"
)

print_table(
    "PRODUCTS TABLE",
    "SELECT * FROM products"
)

print_table(
    "TRANSACTIONS TABLE",
    "SELECT * FROM transactions"
)

print_table(
    "MESSAGES TABLE",
    "SELECT * FROM messages"
)

# ================= CLOSE =================

conn.close()

print("\nDATABASE CHECK COMPLETE")