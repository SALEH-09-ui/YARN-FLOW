import sqlite3

# ================= CONNECT DATABASE =================

conn = sqlite3.connect("yarnflow.db")

cur = conn.cursor()

# ================= USERS TABLE =================

cur.execute("""

CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    mobile TEXT UNIQUE NOT NULL,

    nid TEXT NOT NULL,

    password TEXT NOT NULL

)

""")

# ================= PRODUCTS TABLE =================

cur.execute("""

CREATE TABLE IF NOT EXISTS products(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,

    stock INTEGER NOT NULL,

    price INTEGER NOT NULL

)

""")

# ================= TRANSACTIONS TABLE =================

cur.execute("""

CREATE TABLE IF NOT EXISTS transactions(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    date TEXT NOT NULL,

    product TEXT NOT NULL,

    qty INTEGER NOT NULL,

    paid INTEGER NOT NULL,

    due INTEGER NOT NULL

)

""")

# ================= MESSAGES TABLE =================

cur.execute("""

CREATE TABLE IF NOT EXISTS messages(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    message TEXT NOT NULL,

    reply TEXT

)

""")

# ================= DEFAULT PRODUCTS =================

cur.execute("SELECT COUNT(*) FROM products")

count = cur.fetchone()[0]

if count == 0:

    cur.executemany("""

        INSERT INTO products(
            name,
            stock,
            price
        )

        VALUES(?,?,?)

    """, [

        ("16/1 Doublepan", 526, 5000),

        ("42/1 Promax", 820, 6585),

        ("42/1 Ambia", 430, 7632),

        ("50/1 Promax M", 790, 3500),

        ("40/1 Makson", 990, 4557),

        ("80/1 Taqrim", 2270, 5500),

        ("54/1 Moltazim", 2780, 6003)

    ])

# ================= SAVE =================

conn.commit()

conn.close()

print("DATABASE CREATED SUCCESSFULLY")