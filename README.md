# Real-Time Chat Application

A small browser-based chat system with login, private messaging, online-user tracking, and saved conversation history.

## Why it matters

This project demonstrates the basic product flow behind a messaging service: identify a user, deliver messages in real time, and preserve conversations for later.

## What it does

- Authenticates sample users
- Sends private messages with WebSockets
- Shows messages immediately to online users
- Stores users and chat history in SQLite
- Reloads previous conversations

## Technology

Python, Flask, Flask-SocketIO, SQLite, HTML, CSS, and JavaScript.

## Run

```bash
pip install -r requirements.txt
python server.py
```

Open `http://127.0.0.1:8000`. This is a learning prototype; production use would require secure password hashing and stronger session configuration.
