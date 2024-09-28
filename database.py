import sqlite3
print("SQLite version:", sqlite3.sqlite_version)  # SQLite version

import os

# Create a connection to the database file
base_dir = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(base_dir, 'users.db'), check_same_thread=False)
c = conn.cursor()

# Create a table for users with columns for username, password, and diagnoses
def create_user_table():
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT NOT NULL,
                    diagnoses TEXT)''')
    conn.commit()

# Add a new user to the database
def add_user(username, password):
    c.execute('INSERT INTO users (username, password, diagnoses) VALUES (?, ?, ?)', (username, password, ''))
    conn.commit()

# Check if the user exists in the database
def check_user_exists(username):
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    return c.fetchone()

# Verify user credentials during login
def login_user(username, password):
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    return c.fetchone()

# Update the diagnosis for a specific user
def update_diagnosis(username, new_diagnosis):
    c.execute('SELECT diagnoses FROM users WHERE username = ?', (username,))
    existing_diagnosis = c.fetchone()[0]
    
    # Append new diagnosis to the existing diagnosis history
    if existing_diagnosis:
        updated_diagnosis = existing_diagnosis + f", {new_diagnosis}"
    else:
        updated_diagnosis = new_diagnosis

    c.execute('UPDATE users SET diagnoses = ? WHERE username = ?', (updated_diagnosis, username))
    conn.commit()

# Retrieve diagnosis history for a specific user
def get_user_diagnoses(username):
    c.execute('SELECT diagnoses FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    return result[0] if result else None

# Create the tables on initialization
create_user_table()