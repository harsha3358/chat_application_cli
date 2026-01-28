from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, emit
from database import get_db, init_db
from models import Message

app = Flask(__name__)
app.secret_key = "secret"
socketio = SocketIO(app, async_mode="threading")

init_db()

online_users = {}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cur.fetchone()
        db.close()

        if user:
            session["username"] = username
            return redirect("/chat")

    return render_template("login.html")

@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect("/")
    return render_template("chat.html", username=session["username"])

@socketio.on("connect")
def on_connect():
    if "username" in session:
        online_users[session["username"]] = request.sid

@socketio.on("disconnect")
def on_disconnect():
    if "username" in session:
        online_users.pop(session["username"], None)

@socketio.on("send_message")
def send_message(data):
    sender = session["username"]
    receiver = data["receiver"]
    content = data["message"]

    msg = Message(sender, receiver, content)

    db = get_db()
    cur = db.cursor()

    delivered = 0
    if receiver in online_users:
        emit("receive_message", {
            "sender": sender,
            "message": content,
            "timestamp": msg.timestamp
        }, room=online_users[receiver])
        delivered = 1

    # 🔥 Echo back to sender
    emit("receive_message", {
        "sender": sender,
        "message": content,
        "timestamp": msg.timestamp
    }, room=request.sid)

    cur.execute(
        "INSERT INTO messages VALUES (NULL,?,?,?,?,?)",
        (sender, receiver, content, msg.timestamp, delivered)
    )
    db.commit()
    db.close()

@socketio.on("load_history")
def load_history(data):
    user = session["username"]
    partner = data["partner"]

    db = get_db()
    cur = db.cursor()
    cur.execute("""
    SELECT sender, content, timestamp
    FROM messages
    WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?)
    ORDER BY timestamp
    """, (user, partner, partner, user))

    history = cur.fetchall()
    db.close()

    emit("chat_history", history)

if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=8000, debug=True)
