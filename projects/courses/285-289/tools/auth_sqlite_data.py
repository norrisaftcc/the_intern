"""
User data management module using SQLite storage
This module handles all data operations for the authentication system

CSC285/CTS289 Example - Authentication with SQLite Storage
"""
import sqlite3
import hashlib
import os
from datetime import datetime

# Database file
DB_FILE = "users.db"

def initialize_database():
    """
    Initialize the SQLite database and create tables if they don't exist
    """
    # Create the database file if it doesn't exist
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        email TEXT,
        full_name TEXT,
        created_at TEXT NOT NULL,
        last_login TEXT
    )
    ''')
    
    conn.commit()
    conn.close()
    
    if not os.path.exists(DB_FILE):
        print(f"Created new database: {DB_FILE}")
    else:
        print(f"Connected to existing database: {DB_FILE}")

def hash_password(password):
    """
    Create a simple hash of the password
    Note: This is a basic implementation for educational purposes only
    A real application should use a proper password hashing library like bcrypt
    
    Args:
        password (str): The password to hash
        
    Returns:
        str: The hashed password
    """
    # In a real application, you would use a salt and a proper password hashing algorithm
    # This is a simple hash for demonstration purposes only
    return hashlib.sha256(password.encode()).hexdigest()

def user_exists(username):
    """
    Check if a user with the given username already exists
    
    Args:
        username (str): Username to check
        
    Returns:
        bool: True if user exists, False otherwise
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE LOWER(username) = LOWER(?)", (username,))
    count = cursor.fetchone()[0]
    
    conn.close()
    
    return count > 0

def register_user(username, password, email, full_name):
    """
    Register a new user
    
    Args:
        username (str): User's username
        password (str): User's password (will be hashed)
        email (str): User's email
        full_name (str): User's full name
        
    Returns:
        tuple: (success, message)
    """
    # Basic validation
    if not username or not password:
        return False, "Username and password are required"
    
    if user_exists(username):
        return False, f"Username '{username}' is already taken"
    
    # Hash the password
    password_hash = hash_password(password)
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Insert the new user
        cursor.execute('''
        INSERT INTO users (username, password_hash, email, full_name, created_at)
        VALUES (?, ?, ?, ?, ?)
        ''', (username, password_hash, email, full_name, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        return True, f"User '{username}' registered successfully"
    
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"

def authenticate_user(username, password):
    """
    Authenticate a user
    
    Args:
        username (str): User's username
        password (str): User's password
        
    Returns:
        tuple: (success, user_data or error_message)
    """
    if not username or not password:
        return False, "Username and password are required"
    
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        cursor = conn.cursor()
        
        # Find user by username
        cursor.execute('''
        SELECT id, username, password_hash, email, full_name, created_at, last_login
        FROM users
        WHERE LOWER(username) = LOWER(?)
        ''', (username,))
        
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return False, f"User '{username}' not found"
        
        # Check password
        if user['password_hash'] == hash_password(password):
            # Update last login time
            now = datetime.now().isoformat()
            cursor.execute('''
            UPDATE users SET last_login = ? WHERE id = ?
            ''', (now, user['id']))
            
            conn.commit()
            
            # Convert Row to dict and remove password_hash
            user_dict = dict(user)
            user_dict.pop('password_hash')
            
            conn.close()
            return True, user_dict
        else:
            conn.close()
            return False, "Invalid password"
    
    except sqlite3.Error as e:
        return False, f"Database error: {str(e)}"

def get_user(username):
    """
    Get a user by username
    
    Args:
        username (str): Username to look up
        
    Returns:
        dict or None: User data if found, None otherwise
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, username, email, full_name, created_at, last_login
        FROM users
        WHERE LOWER(username) = LOWER(?)
        ''', (username,))
        
        user = cursor.fetchone()
        
        conn.close()
        
        if user:
            return dict(user)
        else:
            return None
    
    except sqlite3.Error:
        return None

def get_all_users():
    """
    Get all users (without passwords)
    
    Returns:
        list: List of user dictionaries (without passwords)
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, username, email, full_name, created_at, last_login
        FROM users
        ORDER BY created_at DESC
        ''')
        
        users = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return users
    
    except sqlite3.Error:
        return []

# Initialize the database when the module is imported
initialize_database()

if __name__ == "__main__":
    # This code runs when the module is executed directly (not imported)
    # It's useful for testing the module's functionality
    
    print("Testing SQLite user data module...")
    
    # Test registration
    success, message = register_user("sqltestuser", "password123", "sqltest@example.com", "SQL Test User")
    print(f"Registration: {message}")
    
    # Test authentication
    success, result = authenticate_user("sqltestuser", "password123")
    if success:
        print(f"Authentication successful: {result}")
    else:
        print(f"Authentication failed: {result}")
    
    # Failed authentication test
    success, result = authenticate_user("sqltestuser", "wrongpassword")
    if not success:
        print(f"Incorrect password test passed: {result}")
    
    # Display all users
    users = get_all_users()
    print(f"Total users: {len(users)}")
    for user in users:
        print(f"- {user['username']} ({user['email']})")