const API = "http://127.0.0.1:5000";

/* ================= PAGE NAVIGATION ================= */

function show(id){

    document
    .querySelectorAll(".page")
    .forEach(p => p.classList.remove("active"));

    document
    .getElementById(id)
    .classList.add("active");

}

/* ================= GLOBAL VARIABLES ================= */

let currentUser = null;

let editingProductId = null;

let selectedUserId = null;

let selectedMessageId = null;

let editingTransactionId = null;

/* ================= USER SIGNUP ================= */

function signup(){

    if(
        !su_name.value ||
        !su_mobile.value ||
        !su_nid.value ||
        !su_pass.value
    ){
        alert("All fields required");
        return;
    }

    fetch(`${API}/signup`,{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            name:su_name.value.trim(),
            mobile:su_mobile.value.trim(),
            nid:su_nid.value.trim(),
            password:su_pass.value

        })

    })

    .then(res => res.json())

    .then(data => {

        if(data.error){
            alert(data.error);
            return;
        }

        alert("Signup successful");

        su_name.value = "";
        su_mobile.value = "";
        su_nid.value = "";
        su_pass.value = "";

        show("login");

    })

    .catch(() => {
        alert("Signup failed");
    });

}

/* ================= USER LOGIN ================= */

function login(){

    fetch(`${API}/login`,{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            mobile:li_mobile.value,
            password:li_pass.value

        })

    })

    .then(res => res.json())

    .then(user => {

        if(user.error){
            alert(user.error);
            return;
        }

        currentUser = user;

        profileEditName.value = user.name;
        profileEditMobile.value = user.mobile;
        profileEditNid.value = user.nid;

        li_mobile.value = "";
        li_pass.value = "";

        show("dashboard");

    })

    .catch(() => {
        alert("Server error");
    });

}

/* ================= LOGOUT ================= */

function logout(){

    currentUser = null;

    show("welcome");

}

/* ================= PROFILE UPDATE ================= */

function updateProfile(){

    fetch(`${API}/update-profile`,{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            id:currentUser.id,
            name:profileEditName.value,
            mobile:profileEditMobile.value,
            nid:profileEditNid.value

        })

    })

    .then(res => res.json())

    .then(data => {

        alert(data.message);

        currentUser.name = profileEditName.value;
        currentUser.mobile = profileEditMobile.value;
        currentUser.nid = profileEditNid.value;

    });

}

/* ================= USER PRODUCTS ================= */

function loadProducts(){

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

                </tr>

            `;

        });

    });

}

/* ================= USER TRANSACTIONS ================= */

function loadTransactions(){

    if(!currentUser){
        alert("Login first");
        return;
    }

    show("transaction");

    fetch(`${API}/transactions/${currentUser.id}`)

    .then(res => res.json())

    .then(data => {

        transactionTable.innerHTML = "";

        if(data.length === 0){

            transactionTable.innerHTML = `
                <tr>
                    <td colspan="5">No transactions</td>
                </tr>
            `;

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

                </tr>

            `;

        });

    });

}

/* ================= USER MESSAGE ================= */

function sendMessage(){

    if(!userMessage.value){

        alert("Message cannot be empty");

        return;
    }

    fetch(`${API}/message`,{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            user_id:currentUser.id,
            message:userMessage.value.trim()

        })

    })

    .then(res => res.json())

    .then(data => {

        alert(data.message);

        userMessage.value = "";

        loadUserMessages();

    });

}

function loadUserMessages(){

    show("message");

    fetch(`${API}/user/messages/${currentUser.id}`)

    .then(res => res.json())

    .then(data => {

        messageList.innerHTML = "";

        if(data.length === 0){

            messageList.innerHTML = `
                <p>No messages yet</p>
            `;

            return;
        }

        data.forEach(m => {

            messageList.innerHTML += `

                <div>

                    <b>You:</b>
                    ${m.message}

                    <br><br>

                    <b>Admin Reply:</b>
                    ${m.reply || "No reply yet"}

                </div>

            `;

        });

    });

}

/* ================= ADMIN LOGIN ================= */

function adminLogin(){

    fetch(`${API}/admin/login`,{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            username:adminUser.value,
            password:adminPass.value

        })

    })

    .then(res => res.json())

    .then(data => {

        if(data.error){

            alert(data.error);

            return;
        }

        adminUser.value = "";
        adminPass.value = "";

        show("adminDashboard");

    });

}

function adminLogout(){

    show("welcome");

}

/* ================= ADMIN PRODUCTS ================= */

function loadAdminProducts(){

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

                        <button onclick='editProduct(
                            ${p.id},
                            "${p.name}",
                            ${p.stock},
                            ${p.price}
                        )'>

                            Edit

                        </button>

                    </td>

                </tr>

            `;

        });

    });

}

function editProduct(id,name,stock,price){

    editingProductId = id;

    pname.value = name;

    pqty.value = stock;

    pprice.value = price;

}

function saveProduct(){

    if(
        !pname.value ||
        !pqty.value ||
        !pprice.value
    ){
        alert("All fields required");
        return;
    }

    fetch(`${API}/admin/product`,{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            id:editingProductId,
            name:pname.value.trim(),
            stock:Number(pqty.value),
            price:Number(pprice.value)

        })

    })

    .then(res => res.json())

    .then(data => {

        alert(data.message);

        editingProductId = null;

        pname.value = "";
        pqty.value = "";
        pprice.value = "";

        loadAdminProducts();

    });

}

/* ================= ADMIN USERS ================= */

function loadUsers(){

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

                        <button onclick="viewUserTransactions(${u.id})">

                            View

                        </button>

                    </td>

                </tr>

            `;

        });

    });

}

/* ================= VIEW USER TRANSACTIONS ================= */

function viewUserTransactions(uid){

    selectedUserId = uid;

    selectedUserInfo.textContent =
        "User ID : " + uid;

    show("adminUserTransactions");

    loadUserTransactions(uid);

}

function loadUserTransactions(uid){

    fetch(`${API}/transactions/${uid}`)

    .then(res => res.json())

    .then(data => {

        adminTransactionTable.innerHTML = "";

        if(data.length === 0){

            adminTransactionTable.innerHTML = `
                <tr>
                    <td colspan="6">No transactions</td>
                </tr>
            `;

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

                    <td>

                        <button onclick='editTransaction(
                            ${t.id},
                            "${t.date}",
                            "${t.product}",
                            ${t.qty},
                            ${t.paid},
                            ${t.due}
                        )'>

                            Edit

                        </button>

                    </td>

                </tr>

            `;

        });

    });

}

/* ================= EDIT TRANSACTION ================= */

function editTransaction(
    id,
    date,
    product,
    qty,
    paid,
    due
){

    editingTransactionId = id;

    tdate.value = date;
    tproduct.value = product;
    tqty.value = qty;
    tpaid.value = paid;
    tdue.value = due;

}

/* ================= SAVE TRANSACTION ================= */

function saveTransaction(){

    if(!selectedUserId){

        alert("Select user first");

        return;
    }

    fetch(`${API}/admin/transaction`,{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            id:editingTransactionId,
            user_id:selectedUserId,
            date:tdate.value,
            product:tproduct.value.trim(),
            qty:Number(tqty.value),
            paid:Number(tpaid.value || 0),
            due:Number(tdue.value || 0)

        })

    })

    .then(res => res.json())

    .then(data => {

        alert(data.message);

        editingTransactionId = null;

        tdate.value = "";
        tproduct.value = "";
        tqty.value = "";
        tpaid.value = "";
        tdue.value = "";

        loadUserTransactions(selectedUserId);

    });

}

/* ================= ADMIN MESSAGES ================= */

function loadAdminMessages(){

    show("adminMessage");

    fetch(`${API}/admin/messages`)

    .then(res => res.json())

    .then(data => {

        adminMessageTable.innerHTML = "";

        if(data.length === 0){

            adminMessageTable.innerHTML = `
                <tr>
                    <td colspan="3">No messages</td>
                </tr>
            `;

            return;
        }

        data.forEach(m => {

            adminMessageTable.innerHTML += `

                <tr onclick="selectMessage(${m.id})">

                    <td>${m.name}</td>

                    <td>${m.message}</td>

                    <td>${m.reply || "-"}</td>

                </tr>

            `;

        });

    });

}

function selectMessage(id){

    selectedMessageId = id;

}

/* ================= SEND REPLY ================= */

function sendReply(){

    if(
        !selectedMessageId ||
        !adminReply.value
    ){
        alert("Select message and write reply");
        return;
    }

    fetch(`${API}/admin/reply`,{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            message_id:selectedMessageId,
            reply:adminReply.value.trim()

        })

    })

    .then(res => res.json())

    .then(data => {

        alert(data.message);

        adminReply.value = "";

        selectedMessageId = null;

        loadAdminMessages();

    });

}

/* ================= INIT ================= */

let tdate;
let tproduct;
let tqty;
let tpaid;
let tdue;

document.addEventListener("DOMContentLoaded",()=>{

    tdate = document.getElementById("tdate");
    tproduct = document.getElementById("tproduct");
    tqty = document.getElementById("tqty");
    tpaid = document.getElementById("tpaid");
    tdue = document.getElementById("tdue");

    show("welcome");

});