import sqlite3

conn = sqlite3.connect("chat.db")
cur = conn.cursor()

cur.execute("INSERT OR IGNORE INTO users VALUES (?,?)", ("venu", "123"))
cur.execute("INSERT OR IGNORE INTO users VALUES (?,?)", ("bob", "123"))

conn.commit()
conn.close()

print("Users created")
