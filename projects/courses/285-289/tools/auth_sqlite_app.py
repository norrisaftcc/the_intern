"""
Authentication Example Application using SQLite Storage
This Streamlit app demonstrates a login/registration system with database storage

CSC285/CTS289 Example - Authentication with SQLite Storage
"""
import streamlit as st
import auth_sqlite_data as auth_data
import sqlite3
import pandas as pd
from datetime import datetime

# Configure the Streamlit page
st.set_page_config(
    page_title="Auth Example - SQLite Storage",
    page_icon="🔐",
    layout="centered"
)

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "error_message" not in st.session_state:
    st.session_state.error_message = ""

if "success_message" not in st.session_state:
    st.session_state.success_message = ""

# Functions for state management
def login_user(username, password):
    """Handle user login"""
    success, result = auth_data.authenticate_user(username, password)
    
    if success:
        st.session_state.logged_in = True
        st.session_state.current_user = result
        st.session_state.error_message = ""
        return True
    else:
        st.session_state.error_message = result
        return False

def logout_user():
    """Handle user logout"""
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.success_message = "You have been logged out."

def register_new_user(username, password, email, full_name):
    """Handle user registration"""
    success, message = auth_data.register_user(username, password, email, full_name)
    
    if success:
        st.session_state.success_message = message
        return True
    else:
        st.session_state.error_message = message
        return False

# Create sidebar with app information
with st.sidebar:
    st.title("Authentication Demo")
    st.markdown("""
    This application demonstrates an authentication system using SQLite for data storage.
    
    **Features:**
    - User registration
    - Login authentication with password hashing
    - Session management
    - Basic user dashboard
    - Database storage
    
    **Implementation Details:**
    - User data stored in SQLite database
    - Password hashing for security
    - Separation of UI and data logic
    """)
    
    # Show educational note about modularization
    st.subheader("Code Organization")
    st.info("""
    Notice how the code is organized into two separate files:
    
    1. **auth_sqlite_app.py** - User interface and app logic
    2. **auth_sqlite_data.py** - Data handling and storage
    
    The UI code is identical to the JSON version, but the data layer
    has been completely changed to use SQLite. This demonstrates the
    power of separation of concerns.
    """)
    
    # SQL vs JSON comparison
    st.subheader("SQLite vs. JSON")
    st.markdown("""
    **Advantages of SQLite:**
    - Better data integrity
    - Query capabilities (SQL)
    - Scales better with more users
    - Transaction support
    - Better performance for large datasets
    
    **Advantages of JSON:**
    - Simpler to implement
    - Human-readable data files
    - No database setup required
    - Easier to inspect and modify manually
    """)
    
    # Add a count of registered users
    st.subheader("Statistics")
    users = auth_data.get_all_users()
    st.metric("Registered Users", len(users))

# Main application
def main():
    # Display any error or success messages
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
        st.session_state.error_message = ""
    
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = ""
    
    # Check if user is logged in
    if st.session_state.logged_in:
        show_dashboard()
    else:
        show_login_page()

def show_login_page():
    """Show the login and registration interface"""
    st.title("Welcome")
    
    # Create tabs for login and registration
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    # Login tab
    with tab1:
        st.subheader("Login")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                login_user(username, password)
                # Use rerun to update the UI based on login state
                st.experimental_rerun()
    
    # Registration tab
    with tab2:
        st.subheader("Create New Account")
        
        with st.form("registration_form"):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            email = st.text_input("Email")
            full_name = st.text_input("Full Name")
            
            register_button = st.form_submit_button("Register")
            
            if register_button:
                if new_password != confirm_password:
                    st.session_state.error_message = "Passwords do not match"
                else:
                    if register_new_user(new_username, new_password, email, full_name):
                        st.info("Registration successful! You can now login.")
                        # Don't rerun here to let the user see the success message

def show_dashboard():
    """Show the user dashboard after successful login"""
    user = st.session_state.current_user
    
    st.title(f"Welcome, {user['full_name']}")
    st.subheader("User Dashboard")
    
    # Display user information
    st.write(f"**Username:** {user['username']}")
    st.write(f"**Email:** {user['email']}")
    
    # Format dates nicely
    if user.get('created_at'):
        created_date = user['created_at'].split('T')[0]  # Simple date formatting
        st.write(f"**Account Created:** {created_date}")
    
    if user.get('last_login'):
        login_date = user['last_login'].split('T')[0]
        login_time = user['last_login'].split('T')[1][:8]  # Take just the time part
        st.write(f"**Last Login:** {login_date} at {login_time}")
    
    # Add some dashboard functionalities
    st.subheader("Account Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("Edit Profile", disabled=True)
        st.button("Change Password", disabled=True)
    
    with col2:
        st.button("Privacy Settings", disabled=True)
        if st.button("Logout"):
            logout_user()
            st.experimental_rerun()
    
    # Database explorer section (educational)
    with st.expander("Database Explorer (Educational)"):
        st.subheader("SQLite Database Structure")
        st.code("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT,
    full_name TEXT,
    created_at TEXT NOT NULL,
    last_login TEXT
)
        """)
        
        # Show all users (admin-like view)
        st.subheader("All Users (Admin View)")
        
        try:
            conn = sqlite3.connect("users.db")
            query = """
            SELECT id, username, email, full_name, created_at, last_login 
            FROM users
            ORDER BY created_at DESC
            """
            
            df = pd.read_sql_query(query, conn)
            
            # Format the dates
            for date_col in ['created_at', 'last_login']:
                if date_col in df.columns:
                    df[date_col] = df[date_col].apply(lambda x: x.split('T')[0] if isinstance(x, str) and 'T' in x else x)
            
            st.dataframe(df)
            conn.close()
            
        except sqlite3.Error as e:
            st.error(f"Error reading database: {str(e)}")
    
    # Add some example content
    st.subheader("Activity")
    st.info("This is a placeholder for user activity. In a real application, this could show recent actions, notifications, etc.")
    
    # Show a table of recent logins (fake data)
    today = datetime.now()
    login_data = {
        "Date": [
            today.strftime("%Y-%m-%d %H:%M"),
            (today - pd.Timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
            (today - pd.Timedelta(days=3)).strftime("%Y-%m-%d %H:%M"),
        ],
        "IP Address": [
            "192.168.1.1",
            "192.168.1.1",
            "192.168.1.2",
        ],
        "Device": [
            "Desktop - Chrome",
            "Desktop - Chrome",
            "Mobile - Safari",
        ]
    }
    
    login_df = pd.DataFrame(login_data)
    st.write("Recent Logins:")
    st.dataframe(login_df)

if __name__ == "__main__":
    main()