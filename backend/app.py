from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)

CORS(app)

DB = "yarnflow.db"

# ================= DATABASE =================

def get_db():

    conn = sqlite3.connect(DB)

    conn.row_factory = sqlite3.Row

    return conn

# ================= USER SIGNUP =================

@app.route("/signup", methods=["POST"])
def signup():

    d = request.json

    conn = get_db()

    cur = conn.cursor()

    try:

        cur.execute("""

            INSERT INTO users(
                name,
                mobile,
                nid,
                password
            )

            VALUES(?,?,?,?)

        """, (

            d["name"],
            d["mobile"],
            d["nid"],
            d["password"]

        ))

        conn.commit()

        conn.close()

        return jsonify({
            "message":"Signup successful"
        })

    except:

        conn.close()

        return jsonify({
            "error":"Mobile already exists"
        })

# ================= USER LOGIN =================

@app.route("/login", methods=["POST"])
def login():

    d = request.json

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""

        SELECT
            id,
            name,
            mobile,
            nid

        FROM users

        WHERE mobile=? AND password=?

    """, (

        d["mobile"],
        d["password"]

    ))

    user = cur.fetchone()

    conn.close()

    if user:

        return jsonify(dict(user))

    return jsonify({
        "error":"Invalid login"
    })

# ================= UPDATE PROFILE =================

@app.route("/update-profile", methods=["POST"])
def update_profile():

    d = request.json

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""

        UPDATE users

        SET
            name=?,
            mobile=?,
            nid=?

        WHERE id=?

    """, (

        d["name"],
        d["mobile"],
        d["nid"],
        d["id"]

    ))

    conn.commit()

    conn.close()

    return jsonify({
        "message":"Profile updated"
    })

# ================= ADMIN LOGIN =================

@app.route("/admin/login", methods=["POST"])
def admin_login():

    d = request.json

    if (
        d["username"] == "admin"
        and
        d["password"] == "admin123"
    ):

        return jsonify({
            "message":"Admin login successful"
        })

    return jsonify({
        "error":"Invalid admin login"
    })

# ================= GET PRODUCTS =================

@app.route("/products")
def get_products():

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""

        SELECT *

        FROM products

        ORDER BY id DESC

    """)

    data = [dict(r) for r in cur.fetchall()]

    conn.close()

    return jsonify(data)

# ================= SAVE PRODUCT =================

@app.route("/admin/product", methods=["POST"])
def save_product():

    d = request.json

    conn = get_db()

    cur = conn.cursor()

    # UPDATE PRODUCT

    if d.get("id"):

        cur.execute("""

            UPDATE products

            SET
                name=?,
                stock=?,
                price=?

            WHERE id=?

        """, (

            d["name"],
            d["stock"],
            d["price"],
            d["id"]

        ))

    # INSERT PRODUCT

    else:

        cur.execute("""

            INSERT INTO products(
                name,
                stock,
                price
            )

            VALUES(?,?,?)

        """, (

            d["name"],
            d["stock"],
            d["price"]

        ))

    conn.commit()

    conn.close()

    return jsonify({
        "message":"Product saved"
    })

# ================= ADMIN USERS =================

@app.route("/admin/users")
def admin_users():

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""

        SELECT
            id,
            name,
            mobile

        FROM users

        ORDER BY id DESC

    """)

    users = [dict(r) for r in cur.fetchall()]

    conn.close()

    return jsonify(users)

# ================= USER TRANSACTIONS =================

@app.route("/transactions/<int:user_id>")
def get_transactions(user_id):

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""

        SELECT *

        FROM transactions

        WHERE user_id=?

        ORDER BY id DESC

    """, (user_id,))

    data = [dict(r) for r in cur.fetchall()]

    conn.close()

    return jsonify(data)

# ================= SAVE TRANSACTION =================

@app.route("/admin/transaction", methods=["POST"])
def save_transaction():

    d = request.json

    conn = get_db()

    cur = conn.cursor()

    # UPDATE TRANSACTION

    if d.get("id"):

        cur.execute("""

            UPDATE transactions

            SET
                date=?,
                product=?,
                qty=?,
                paid=?,
                due=?

            WHERE id=?

        """, (

            d["date"],
            d["product"],
            d["qty"],
            d["paid"],
            d["due"],
            d["id"]

        ))

    # INSERT TRANSACTION

    else:

        cur.execute("""

            INSERT INTO transactions(

                user_id,
                date,
                product,
                qty,
                paid,
                due

            )

            VALUES(?,?,?,?,?,?)

        """, (

            d["user_id"],
            d["date"],
            d["product"],
            d["qty"],
            d["paid"],
            d["due"]

        ))

    conn.commit()

    conn.close()

    return jsonify({
        "message":"Transaction saved"
    })

# ================= SEND MESSAGE =================

@app.route("/message", methods=["POST"])
def send_message():

    d = request.json

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""

        INSERT INTO messages(

            user_id,
            message

        )

        VALUES(?,?)

    """, (

        d["user_id"],
        d["message"]

    ))

    conn.commit()

    conn.close()

    return jsonify({
        "message":"Message sent"
    })

# ================= USER MESSAGE LIST =================

@app.route("/user/messages/<int:user_id>")
def user_messages(user_id):

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""

        SELECT
            message,
            reply

        FROM messages

        WHERE user_id=?

        ORDER BY id DESC

    """, (user_id,))

    data = [dict(r) for r in cur.fetchall()]

    conn.close()

    return jsonify(data)

# ================= ADMIN MESSAGE LIST =================

@app.route("/admin/messages")
def admin_messages():

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""

        SELECT

            m.id,
            u.name,
            m.message,
            m.reply

        FROM messages m

        JOIN users u
        ON m.user_id = u.id

        ORDER BY m.id DESC

    """)

    data = [dict(r) for r in cur.fetchall()]

    conn.close()

    return jsonify(data)

# ================= ADMIN REPLY =================

@app.route("/admin/reply", methods=["POST"])
def admin_reply():

    d = request.json

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""

        UPDATE messages

        SET reply=?

        WHERE id=?

    """, (

        d["reply"],
        d["message_id"]

    ))

    conn.commit()

    conn.close()

    return jsonify({
        "message":"Reply sent"
    })

# ================= RUN =================

if __name__ == "__main__":

    app.run(debug=True)