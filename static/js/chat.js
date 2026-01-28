const socket = io();
let currentPartner = "";

function openChat() {
    currentPartner = document.getElementById("partner").value;
    socket.emit("load_history", { partner: currentPartner });
}

function sendMessage() {
    const msg = document.getElementById("message").value;
    if (!msg || !currentPartner) return;

    socket.emit("send_message", {
        receiver: currentPartner,
        message: msg
    });

    document.getElementById("message").value = "";
}

socket.on("receive_message", data => {
    const div = document.createElement("div");
    if (data.sender === USERNAME) {
        div.innerHTML = "<b>You:</b> " + data.message;
    } else {
        div.innerHTML = "<b>" + data.sender + ":</b> " + data.message;
    }
    document.getElementById("messages").appendChild(div);
});

socket.on("chat_history", history => {
    const messages = document.getElementById("messages");
    messages.innerHTML = "";

    history.forEach(m => {
        const div = document.createElement("div");
        if (m[0] === USERNAME) {
            div.innerHTML = "<b>You:</b> " + m[1];
        } else {
            div.innerHTML = "<b>" + m[0] + ":</b> " + m[1];
        }
        messages.appendChild(div);
    });
});
