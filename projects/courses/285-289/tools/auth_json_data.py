"""
User data management module using JSON storage
This module handles all data operations for the authentication system

CSC285/CTS289 Example - Basic Authentication with JSON Storage
"""
import json
import os
from datetime import datetime

# File path for our user data
USERS_FILE = "users.json"

def initialize_data():
    """
    Initialize the JSON data file if it doesn't exist
    """
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump({"users": []}, f)
        print(f"Created new users file: {USERS_FILE}")
    else:
        print(f"Using existing users file: {USERS_FILE}")

def load_users():
    """
    Load users from the JSON file
    
    Returns:
        list: List of user dictionaries
    """
    try:
        with open(USERS_FILE, 'r') as f:
            data = json.load(f)
            return data.get("users", [])
    except (json.JSONDecodeError, FileNotFoundError):
        # Handle corrupted or missing file by creating a new one
        initialize_data()
        return []

def save_users(users):
    """
    Save users to the JSON file
    
    Args:
        users (list): List of user dictionaries to save
    """
    with open(USERS_FILE, 'w') as f:
        json.dump({"users": users}, f, indent=2)

def user_exists(username):
    """
    Check if a user with the given username already exists
    
    Args:
        username (str): Username to check
        
    Returns:
        bool: True if user exists, False otherwise
    """
    users = load_users()
    return any(user['username'].lower() == username.lower() for user in users)

def register_user(username, password, email, full_name):
    """
    Register a new user
    
    Args:
        username (str): User's username
        password (str): User's password (Note: stored in plaintext for this example only)
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
    
    # Load existing users
    users = load_users()
    
    # Create new user
    # NOTE: In a real application, NEVER store passwords in plaintext!
    # This is for demonstration purposes only.
    new_user = {
        "username": username,
        "password": password,  # INSECURE: For educational purposes only
        "email": email,
        "full_name": full_name,
        "created_at": datetime.now().isoformat(),
        "last_login": None
    }
    
    # Add to users list
    users.append(new_user)
    
    # Save updated user list
    save_users(users)
    
    return True, f"User '{username}' registered successfully"

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
    
    users = load_users()
    
    # Find user by username
    for user in users:
        if user['username'].lower() == username.lower():
            # Check password (insecure comparison for demo only)
            if user['password'] == password:
                # Update last login time
                user['last_login'] = datetime.now().isoformat()
                save_users(users)
                
                # Return user data (without password)
                user_data = user.copy()
                user_data.pop('password')
                return True, user_data
            else:
                return False, "Invalid password"
    
    return False, f"User '{username}' not found"

def get_user(username):
    """
    Get a user by username
    
    Args:
        username (str): Username to look up
        
    Returns:
        dict or None: User data if found, None otherwise
    """
    users = load_users()
    
    for user in users:
        if user['username'].lower() == username.lower():
            # Return user data (without password)
            user_data = user.copy()
            user_data.pop('password')
            return user_data
    
    return None

def get_all_users():
    """
    Get all users (without passwords)
    
    Returns:
        list: List of user dictionaries (without passwords)
    """
    users = load_users()
    
    # Remove passwords from all users
    for user in users:
        if 'password' in user:
            user.pop('password')
    
    return users

# Initialize the data file when the module is imported
initialize_data()

if __name__ == "__main__":
    # This code runs when the module is executed directly (not imported)
    # It's useful for testing the module's functionality
    
    print("Testing user data module...")
    
    # Test registration
    success, message = register_user("testuser", "password123", "test@example.com", "Test User")
    print(f"Registration: {message}")
    
    # Test authentication
    success, result = authenticate_user("testuser", "password123")
    if success:
        print(f"Authentication successful: {result}")
    else:
        print(f"Authentication failed: {result}")
    
    # Display all users
    users = get_all_users()
    print(f"Total users: {len(users)}")
    for user in users:
        print(f"- {user['username']} ({user['email']})")