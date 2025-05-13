"""
Database Setup Script for SQLite Authentication Example
This script initializes the SQLite database and creates test users

CSC285/CTS289 Example - Authentication with SQLite Storage
"""
import sqlite3
import os
import hashlib
from datetime import datetime, timedelta

# Database file
DB_FILE = "users.db"

def hash_password(password):
    """Create a simple hash of the password"""
    return hashlib.sha256(password.encode()).hexdigest()

def setup_database():
    """Set up the database and create test users"""
    # Remove existing database file if it exists
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Removed existing database: {DB_FILE}")
    
    # Create a new database connection
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        email TEXT,
        full_name TEXT,
        created_at TEXT NOT NULL,
        last_login TEXT
    )
    ''')
    
    # Create test users
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    
    test_users = [
        (
            "demo_user",
            hash_password("password123"),
            "demo@example.com",
            "Demo User",
            today.isoformat(),
            yesterday.isoformat()
        ),
        (
            "admin",
            hash_password("admin123"),
            "admin@example.com",
            "Admin User",
            today.isoformat(),
            yesterday.isoformat()
        ),
        (
            "student",
            hash_password("student123"),
            "student@example.com",
            "Student User",
            today.isoformat(),
            yesterday.isoformat()
        )
    ]
    
    cursor.executemany('''
    INSERT INTO users (username, password_hash, email, full_name, created_at, last_login)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', test_users)
    
    # Commit changes and close connection
    conn.commit()
    
    # Verify the database setup
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    print(f"Database created: {DB_FILE}")
    print(f"Test users created: {user_count}")
    
    # List the users
    cursor.execute("SELECT id, username, email FROM users")
    users = cursor.fetchall()
    
    print("\nAvailable test users:")
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}")
    
    conn.close()

if __name__ == "__main__":
    setup_database()
    print("\nDatabase setup complete. You can now run the authentication example.")
    print("Login with username 'demo_user' and password 'password123'")