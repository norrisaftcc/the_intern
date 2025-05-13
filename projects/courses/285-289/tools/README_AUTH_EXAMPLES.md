# Authentication Example Programs

This directory contains example programs demonstrating user authentication (login/registration) implementation with increasing levels of sophistication. These examples showcase important software engineering concepts like modularization, different persistence approaches, and separation of concerns.

## Learning Objectives

These examples are designed to teach:

1. **Modularization** - Separating code into logical components
2. **Data Persistence** - Storing and retrieving user data
3. **UI Development** - Creating simple but functional interfaces
4. **Security Basics** - Safe password storage, validation, etc.
5. **Refactoring** - Evolving code to use better practices

## Example Programs

### 1. Basic Authentication (JSON Storage)

**Files:**
- `auth_json_app.py` - Main Streamlit application
- `auth_json_data.py` - Data handling with JSON file storage
- `users.json` - Sample data file

**Features:**
- Simple login and registration functionality
- JSON file-based user storage
- Basic validation
- Password storage (insecure, for demonstration only)

### 2. Improved Authentication (SQLite Storage)

**Files:**
- `auth_sqlite_app.py` - Main Streamlit application
- `auth_sqlite_data.py` - Data handling with SQLite
- `db_setup.py` - Database initialization script
- `users.db` - SQLite database (generated)

**Features:**
- Same UI as the JSON version
- SQLite database storage
- Improved validation
- Basic password hashing

### 3. Advanced Authentication (Modular Architecture)

**Files:**
- `auth_advanced/`
  - `__init__.py`
  - `app.py` - Main application
  - `data/`
    - `__init__.py`
    - `user_repository.py` - User data access
    - `db_connector.py` - Database connection handling
  - `ui/`
    - `__init__.py`
    - `login_page.py` - Login UI components
    - `register_page.py` - Registration UI components
    - `dashboard_page.py` - Post-login UI
  - `models/`
    - `__init__.py`
    - `user.py` - User model
  - `utils/`
    - `__init__.py`
    - `password_utils.py` - Password handling
    - `validation.py` - Input validation

**Features:**
- Full modular architecture
- Proper password hashing with salt
- Comprehensive validation
- Session management
- Role-based features

## Teaching Approach

1. **Start Simple**: Begin with the JSON version to teach basic concepts
2. **Compare & Contrast**: Show how the same functionality can be implemented with different storage mechanisms
3. **Explain Modularization**: Use the advanced version to demonstrate proper code organization
4. **Guided Exercises**: Provide exercises where students enhance the examples (add features, fix issues)

## Implementation Notes

### Authentication Flow

All examples implement this basic flow:

1. **Registration**
   - Collect username, password, and basic user info
   - Validate inputs
   - Check if username already exists
   - Store user data
   - Redirect to login

2. **Login**
   - Collect username and password
   - Validate credentials
   - Create session
   - Redirect to dashboard

3. **Dashboard**
   - Show logged-in user information
   - Provide logout functionality
   - Display different features based on user role (advanced example)

### Security Considerations

These examples are for educational purposes. Important security notes:

- The JSON example uses plaintext passwords - explicitly teach that this is ONLY for learning
- The SQLite example introduces basic hashing but lacks proper salt handling
- The advanced example demonstrates proper security practices
- Emphasize that production applications need additional security measures

## Use as Teaching Material

These examples can be used in the following ways:

1. **Code Walkthrough**: Guide students through each version, explaining the enhancements
2. **Incremental Development**: Have students start with the JSON version and upgrade it to SQLite
3. **Refactoring Exercise**: Have students convert the SQLite version to the modular architecture
4. **Feature Addition**: Assign students to add features like password reset, email verification, etc.

## Future Enhancements

Ideas for students to extend these examples:

1. Add email verification
2. Implement password reset functionality
3. Add two-factor authentication
4. Create user profile management
5. Add JWT (JSON Web Token) based authentication
6. Implement OAuth integration (Google, GitHub, etc.)
7. Add proper logging and error handling
8. Create an admin panel for user management