
import sqlite3

# Connect to the SQLite3 database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        age INTEGER NOT NULL
    )
''')

# Insert some sample users
sample_users = [
    ('Alice Johnson', 'alice@example.com', 30),
    ('Bob Smith', 'bob@example.com', 25),
    ('Charlie Lee', 'charlie@example.com', 22),
    ('Diana Prince', 'diana@example.com', 35),
    ('Ethan Brown', 'ethan@example.com', 28),
]

cursor.executemany('''
    INSERT OR IGNORE INTO users (name, email, age)
    VALUES (?, ?, ?)
''', sample_users)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and users table created with sample data.")
