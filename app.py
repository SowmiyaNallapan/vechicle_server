from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Create users table if it doesn't exist
def create_users_table():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            dob TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_users_table()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    phone = data.get("phone")
    dob = data.get("dob")
    password = data.get("password")

    if not all([username, email, phone, dob, password]):
        return jsonify({"error": "Missing required fields"}), 400

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    if cur.fetchone():
        conn.close()
        return jsonify({"error": "Email already registered"}), 400

    cur.execute("INSERT INTO users (username, email, phone, dob, password) VALUES (?, ?, ?, ?, ?)", 
                (username, email, phone, dob, password))
    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)
