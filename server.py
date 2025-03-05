import mysql.connector
from flask import Flask, request, send_file
import os

app = Flask(__name__)

# MySQL connection parameters
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

def init_db():
    """
    Initialize the MySQL database:
      - Create the database if it doesn't exist.
      - Drop and create the 'users' table.
      - Insert a default user and additional sample data.
    """
    # Connect without specifying a database to create the database if needed
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
    cursor.execute(f"CREATE DATABASE {DB_NAME}")
    conn.commit()
    cursor.close()
    conn.close()

    # Connect to the newly created database
    conn = get_db()
    cursor = conn.cursor()

    # Create the 'users' table
    create_table_query = """
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    )
    """
    cursor.execute(create_table_query)
    conn.commit()

    # Insert multiple rows into the 'users' table
    insert_query = """
    INSERT INTO users (username, password) VALUES
        ('admin', 'password'),
        ('user1', 'pass1'),
        ('user2', 'pass2'),
        ('user3', 'pass3'),
        ('user4', 'pass4')
    """
    cursor.execute(insert_query)
    conn.commit()

    cursor.close()
    conn.close()

@app.route('/')
def index():
    # Serve the login page
    return send_file("index.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # *** VULNERABLE SQL QUERY (DO NOT USE IN PRODUCTION) ***
    query = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, password)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query)
    user = cursor.fetchone()
    cursor.close()
    conn.close()
   
    if user:
        return f"Login Successful! Welcome , {username}."
    else:
        return "Login Failed! Invalid credentials.", 401

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
