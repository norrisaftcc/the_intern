"""
Authentication Example Application using JSON Storage
This Streamlit app demonstrates a basic login/registration system

CSC285/CTS289 Example - Basic Authentication with JSON Storage
"""
import streamlit as st
import auth_json_data as auth_data

# Configure the Streamlit page
st.set_page_config(
    page_title="Auth Example - JSON Storage",
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
    This application demonstrates a basic authentication system using JSON for data storage.
    
    **Features:**
    - User registration
    - Login authentication
    - Session management
    - Basic user dashboard
    
    **Implementation Details:**
    - User data stored in JSON file
    - Separation of UI and data logic
    - Basic session management with Streamlit
    
    **Security Note:**
    This demo uses plaintext password storage which is **NOT SECURE** and
    should never be used in real applications. This is for educational 
    purposes only.
    """)
    
    # Show educational note about code separation
    st.subheader("Code Organization")
    st.info("""
    Notice how the code is organized into two separate files:
    
    1. **auth_json_app.py** - User interface and app logic
    2. **auth_json_data.py** - Data handling and storage
    
    This separation of concerns makes the code:
    - Easier to maintain
    - More modular
    - More testable
    - Easier to extend
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
    
    # Add some fake dashboard functionalities
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
    
    # Add some example content
    st.subheader("Activity")
    st.info("This is a placeholder for user activity. In a real application, this could show recent actions, notifications, etc.")
    
    # Demonstrate how we would display different content based on user data
    st.subheader("Your Content")
    st.write("This section would display content specific to the logged-in user.")
    
    # Show a table of recent logins (fake data)
    import pandas as pd
    import datetime
    
    # Create some fake login history
    today = datetime.datetime.now()
    login_data = {
        "Date": [
            today.strftime("%Y-%m-%d %H:%M"),
            (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
            (today - datetime.timedelta(days=3)).strftime("%Y-%m-%d %H:%M"),
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