import psycopg2
import os

# PostgreSQL connection parameters
DATABASE_URL = os.getenv("DATABASE_URL", "postgres://postgres:Gc6EeE3AFB1g215651gFbC1Ae6gg3cB4@autorack.proxy.rlwy.net:13643/railway")


# Create a connection to the PostgreSQL database
conn = psycopg2.connect(DATABASE_URL)
c = conn.cursor()

# Create a table for users with columns for username, password, and diagnoses
def create_user_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT NOT NULL,
            diagnoses TEXT
        )
    ''')
    conn.commit()

# Add a new user to the database
def add_user(username, password):
    c.execute('INSERT INTO users (username, password, diagnoses) VALUES (%s, %s, %s)', (username, password, ''))
    conn.commit()

# Check if the user exists in the database
def check_user_exists(username):
    c.execute('SELECT * FROM users WHERE username = %s', (username,))
    return c.fetchone()

# Verify user credentials during login
def login_user(username, password):
    c.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
    return c.fetchone()

# Update the diagnosis for a specific user
def update_diagnosis(username, new_diagnosis):
    c.execute('SELECT diagnoses FROM users WHERE username = %s', (username,))
    existing_diagnosis = c.fetchone()
    if existing_diagnosis and existing_diagnosis[0]:
        updated_diagnosis = existing_diagnosis[0] + f", {new_diagnosis}"
    else:
        updated_diagnosis = new_diagnosis

    c.execute('UPDATE users SET diagnoses = %s WHERE username = %s', (updated_diagnosis, username))
    conn.commit()

# Retrieve diagnosis history for a specific user
def get_user_diagnoses(username):
    c.execute('SELECT diagnoses FROM users WHERE username = %s', (username,))
    result = c.fetchone()
    return result[0] if result else None

# Create the tables on initialization
create_user_table()