from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)

# ================= CORS =================
CORS(app)

# ================= PATHS =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "yarnflow.db")
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

# ================= DB =================
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# ================= FRONTEND SERVE =================
@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def serve_frontend_files(path):
    return send_from_directory(FRONTEND_DIR, path)

# ================= USER AUTH =================
@app.route("/signup", methods=["POST"])
def signup():
    d = request.json

    # 🔴 REQUIRED VALIDATION (FIX)
    required = ["name", "mobile", "nid", "password"]
    for k in required:
        if not d.get(k):
            return jsonify({"error": f"{k} is required"}), 400

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO users (name, mobile, nid, password)
            VALUES (?, ?, ?, ?)
        """, (
            d["name"].strip(),
            d["mobile"].strip(),
            d["nid"].strip(),
            d["password"]
        ))
        conn.commit()
        return jsonify({"message": "Signup successful"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Mobile already exists"}), 400
    finally:
        conn.close()

@app.route("/login", methods=["POST"])
def login():
    d = request.json

    if not d.get("mobile") or not d.get("password"):
        return jsonify({"error": "Mobile and password required"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, mobile, nid
        FROM users
        WHERE mobile=? AND password=?
    """, (d["mobile"], d["password"]))

    user = cur.fetchone()
    conn.close()

    if user:
        return jsonify(dict(user))
    return jsonify({"error": "Invalid login"}), 401

# ================= ADMIN AUTH =================
@app.route("/admin/login", methods=["POST"])
def admin_login():
    d = request.json
    if d.get("username") == "admin" and d.get("password") == "admin123":
        return jsonify({"message": "Admin logged in"})
    return jsonify({"error": "Invalid admin credentials"}), 401

# ================= PRODUCTS =================
@app.route("/products", methods=["GET"])
def get_products():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    data = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(data)

@app.route("/admin/product", methods=["POST"])
def save_product():
    d = request.json

    if not d.get("name") or d.get("stock") is None or d.get("price") is None:
        return jsonify({"error": "Invalid product data"}), 400

    conn = get_db()
    cur = conn.cursor()

    if d.get("id"):
        cur.execute("""
            UPDATE products
            SET name=?, stock=?, price=?
            WHERE id=?
        """, (
            d["name"].strip(),
            int(d["stock"]),
            int(d["price"]),
            int(d["id"])
        ))
    else:
        cur.execute("""
            INSERT INTO products (name, stock, price)
            VALUES (?, ?, ?)
        """, (
            d["name"].strip(),
            int(d["stock"]),
            int(d["price"])
        ))

    conn.commit()
    conn.close()
    return jsonify({"message": "Product saved"})

# ================= USERS (ADMIN VIEW) =================
@app.route("/admin/users")
def admin_users():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name, mobile FROM users")
    data = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(data)

# ================= TRANSACTIONS =================
@app.route("/transactions/<int:user_id>")
def user_transactions(user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT date, product, qty, paid, due
        FROM transactions
        WHERE user_id=?
        ORDER BY id DESC
    """, (user_id,))

    data = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(data)

@app.route("/admin/transaction", methods=["POST"])
def admin_add_transaction():
    d = request.json
    print("ADMIN TRANSACTION PAYLOAD:", d)

    # 🔴 REQUIRED VALIDATION (FIX)
    required = ["user_id", "date", "product", "qty", "paid", "due"]
    for k in required:
        if d.get(k) in [None, ""]:
            return jsonify({"error": f"{k} is required"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO transactions (user_id, date, product, qty, paid, due)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        int(d["user_id"]),
        d["date"].strip(),
        d["product"].strip(),
        int(d["qty"]),
        int(d["paid"]),
        int(d["due"])
    ))

    conn.commit()
    conn.close()
    return jsonify({"message": "Transaction saved"})

# ================= MESSAGES =================
@app.route("/message", methods=["POST"])
def send_message():
    d = request.json

    if not d.get("user_id") or not d.get("message"):
        return jsonify({"error": "Invalid message"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO messages (user_id, message)
        VALUES (?, ?)
    """, (int(d["user_id"]), d["message"].strip()))

    conn.commit()
    conn.close()
    return jsonify({"message": "Message sent"})

@app.route("/admin/messages")
def admin_messages():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT m.id, u.name, m.message, m.reply
        FROM messages m
        JOIN users u ON m.user_id = u.id
        ORDER BY m.id DESC
    """)
    data = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(data)

@app.route("/admin/reply", methods=["POST"])
def reply_message():
    d = request.json

    if not d.get("reply") or not d.get("message_id"):
        return jsonify({"error": "Invalid reply"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE messages
        SET reply=?
        WHERE id=?
    """, (d["reply"].strip(), int(d["message_id"])))

    conn.commit()
    conn.close()
    return jsonify({"message": "Reply sent"})

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
