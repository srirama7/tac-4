import sqlite3
import os

# Create test database
db_path = 'test_users.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    age INTEGER
)
''')

# Insert test data
cursor.executemany('INSERT INTO users (name, email, age) VALUES (?, ?, ?)', [
    ('Alice', 'alice@example.com', 30),
    ('Bob', 'bob@example.com', 25),
    ('Charlie', 'charlie@example.com', 35)
])

conn.commit()
conn.close()
print(f'Created test database: {os.path.abspath(db_path)}')
