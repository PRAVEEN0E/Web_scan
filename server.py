import mysql.connector
from flask import Flask, request, send_file
import os

app = Flask(__name__)

DB_HOST = 'localhost'
DB_USER = 'admin'
DB_PASSWORD = 'Qwertyuiop'
DB_NAME = 'vulnerable_db'

def get_db():
    """Connect to the MySQL database."""
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return conn

@app.route('/')
def index():
    return send_file("index.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    query = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, password)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query)
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return f"Login Successful! Welcome, {username}."
    else:
        return "Login Failed! Invalid credentials."

if __name__ == '__main__':
    app.run(debug=True)
