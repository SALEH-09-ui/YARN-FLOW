const API = "http://127.0.0.1:5000";

/* ================= PAGE NAVIGATION ================= */
function show(id) {
    document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
    document.getElementById(id).classList.add("active");
}

/* ================= GLOBAL STATE ================= */
let currentUser = null;
let editingProductId = null;
let selectedUserId = null;
let selectedMessageId = null;

/* ================= USER SIGNUP ================= */
function signup() {
    if (!su_name.value || !su_mobile.value || !su_nid.value || !su_pass.value) {
        alert("All fields required");
        return;
    }

    fetch(`${API}/signup`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            name: su_name.value.trim(),
            mobile: su_mobile.value.trim(),
            nid: su_nid.value.trim(),
            password: su_pass.value
        })
    })
    .then(res => res.json())
    .then(d => {
        if (d.error) return alert(d.error);
        alert("Signup successful");
        show("login");
    })
    .catch(() => alert("Signup failed"));
}

/* ================= USER LOGIN ================= */
function login() {
    fetch(`${API}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            mobile: li_mobile.value,
            password: li_pass.value
        })
    })
    .then(res => res.json())
    .then(u => {
        if (u.error) return alert(u.error);

        currentUser = u;
        profileName.textContent = u.name;
        profileMobile.textContent = u.mobile;
        profileNid.textContent = u.nid;

        show("dashboard");
    })
    .catch(() => alert("Server error"));
}

function logout() {
    currentUser = null;
    show("welcome");
}

/* ================= USER PRODUCTS ================= */
function loadProducts() {
    show("product");
    fetch(`${API}/products`)
        .then(res => res.json())
        .then(data => {
            productTable.innerHTML = "";
            data.forEach(p => {
                productTable.innerHTML += `
                    <tr>
                        <td>${p.name}</td>
                        <td>${p.stock}</td>
                        <td>৳${p.price}</td>
                    </tr>`;
            });
        });
}

/* ================= USER TRANSACTIONS ================= */
function loadTransactions() {
    if (!currentUser) return alert("Login first");

    show("transaction");
    fetch(`${API}/transactions/${currentUser.id}`)
        .then(res => res.json())
        .then(data => {
            transactionTable.innerHTML = "";
            if (data.length === 0) {
                transactionTable.innerHTML =
                    `<tr><td colspan="5">No transactions</td></tr>`;
                return;
            }
            data.forEach(t => {
                transactionTable.innerHTML += `
                    <tr>
                        <td>${t.date}</td>
                        <td>${t.product}</td>
                        <td>${t.qty}</td>
                        <td>৳${t.paid}</td>
                        <td>৳${t.due}</td>
                    </tr>`;
            });
        });
}

/* ================= USER MESSAGE ================= */
function sendMessage() {
    if (!userMessage.value) {
        alert("Message cannot be empty");
        return;
    }

    fetch(`${API}/message`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            user_id: currentUser.id,
            message: userMessage.value.trim()
        })
    })
    .then(res => res.json())
    .then(() => {
        alert("Message sent");
        userMessage.value = "";
    });
}

/* ================= ADMIN LOGIN ================= */
function adminLogin() {
    fetch(`${API}/admin/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: adminUser.value,
            password: adminPass.value
        })
    })
    .then(res => res.json())
    .then(d => {
        if (d.error) return alert(d.error);
        show("adminDashboard");
    });
}

function adminLogout() {
    show("welcome");
}

/* ================= ADMIN PRODUCTS ================= */
function loadAdminProducts() {
    show("adminProduct");
    fetch(`${API}/products`)
        .then(res => res.json())
        .then(data => {
            adminProductTable.innerHTML = "";
            data.forEach(p => {
                adminProductTable.innerHTML += `
                    <tr>
                        <td>${p.name}</td>
                        <td>${p.stock}</td>
                        <td>৳${p.price}</td>
                        <td>
                            <button onclick="editProduct(${p.id}, '${p.name}', ${p.stock}, ${p.price})">Edit</button>
                        </td>
                    </tr>`;
            });
        });
}

function editProduct(id, name, stock, price) {
    editingProductId = id;
    pname.value = name;
    pqty.value = stock;
    pprice.value = price;
}

function saveProduct() {
    if (!pname.value || !pqty.value || !pprice.value) {
        alert("All product fields required");
        return;
    }

    fetch(`${API}/admin/product`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            id: editingProductId,
            name: pname.value.trim(),
            stock: pqty.value,
            price: pprice.value
        })
    })
    .then(() => {
        editingProductId = null;
        pname.value = pqty.value = pprice.value = "";
        loadAdminProducts();
    });
}

/* ================= ADMIN TRANSACTIONS ================= */
function loadUsers() {
    show("adminTransaction");
    fetch(`${API}/admin/users`)
        .then(res => res.json())
        .then(users => {
            adminUserTable.innerHTML = "";
            users.forEach(u => {
                adminUserTable.innerHTML += `
                    <tr>
                        <td>${u.name}</td>
                        <td>${u.mobile}</td>
                        <td>
                            <button onclick="viewUserTransactions(${u.id})">View</button>
                        </td>
                    </tr>`;
            });
        });
}

function viewUserTransactions(uid) {
    selectedUserId = uid;
    document.getElementById("selectedUserInfo").textContent =
        "Adding transaction for User ID: " + uid;

    show("adminUserTransactions");
    loadUserTransactions(uid);
}

function loadUserTransactions(uid) {
    fetch(`${API}/transactions/${uid}`)
        .then(res => res.json())
        .then(data => {
            adminTransactionTable.innerHTML = "";
            if (data.length === 0) {
                adminTransactionTable.innerHTML =
                    `<tr><td colspan="5">No transactions</td></tr>`;
                return;
            }
            data.forEach(t => {
                adminTransactionTable.innerHTML += `
                    <tr>
                        <td>${t.date}</td>
                        <td>${t.product}</td>
                        <td>${t.qty}</td>
                        <td>৳${t.paid}</td>
                        <td>৳${t.due}</td>
                    </tr>`;
            });
        });
}

function saveTransaction() {
    if (!selectedUserId) {
        alert("Select a user first");
        return;
    }

    if (!tdate.value || !tproduct.value || !tqty.value) {
        alert("All transaction fields required");
        return;
    }

    fetch(`${API}/admin/transaction`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            user_id: selectedUserId,
            date: tdate.value,
            product: tproduct.value.trim(),
            qty: Number(tqty.value),
            paid: Number(tpaid.value || 0),
            due: Number(tdue.value || 0)
        })
    })
    .then(res => res.json())
    .then(() => {
        tdate.value = tproduct.value = tqty.value = tpaid.value = tdue.value = "";
        loadUserTransactions(selectedUserId);
    });
}

/* ================= ADMIN MESSAGES ================= */
function loadAdminMessages() {
    show("adminMessage");

    fetch(`${API}/admin/messages`)
        .then(res => res.json())
        .then(data => {
            adminMessageTable.innerHTML = "";
            if (data.length === 0) {
                adminMessageTable.innerHTML =
                    `<tr><td colspan="3">No messages</td></tr>`;
                return;
            }

            data.forEach(m => {
                adminMessageTable.innerHTML += `
                    <tr onclick="selectMessage(${m.id})">
                        <td>${m.name}</td>
                        <td>${m.message}</td>
                        <td>${m.reply || "-"}</td>
                    </tr>`;
            });
        });
}

function selectMessage(id) {
    selectedMessageId = id;
}

function sendReply() {
    if (!selectedMessageId || !adminReply.value) {
        alert("Select message and write reply");
        return;
    }

    fetch(`${API}/admin/reply`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            message_id: selectedMessageId,
            reply: adminReply.value.trim()
        })
    })
    .then(() => {
        adminReply.value = "";
        selectedMessageId = null;
        loadAdminMessages();
    });
}

/* ================= INIT ================= */
let tdate, tproduct, tqty, tpaid, tdue;

document.addEventListener("DOMContentLoaded", () => {
    tdate = document.getElementById("tdate");
    tproduct = document.getElementById("tproduct");
    tqty = document.getElementById("tqty");
    tpaid = document.getElementById("tpaid");
    tdue = document.getElementById("tdue");
    show("welcome");
});
