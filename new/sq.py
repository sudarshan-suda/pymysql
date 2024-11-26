import streamlit as st
import sqlite3
import subprocess

# SQLite Database setup
def create_connection():
    conn = sqlite3.connect("user_management.db")  # SQLite database file
    conn.row_factory = sqlite3.Row  # Enable dictionary-like cursor access
    return conn

# Create the users table if it doesn't exist
def initialize_database():
    conn = create_connection()
    with conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """)
    conn.close()

# Function to register a new user
def register_user(name, email, password):
    try:
        conn = create_connection()
        with conn:
            conn.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
            )
        st.success("User registered successfully!")
    except sqlite3.IntegrityError:
        st.error("Email already exists. Please try another.")
    except sqlite3.Error as e:
        st.error(f"An error occurred: {e}")
    finally:
        conn.close()

# Function to validate user login
def login_user(email, password):
    try:
        conn = create_connection()
        with conn:
            cursor = conn.execute(
                "SELECT * FROM users WHERE email = ? AND password = ?",
                (email, password)
            )
            user = cursor.fetchone()
        return user
    except sqlite3.Error as e:
        st.error(f"An error occurred: {e}")
        return None
    finally:
        conn.close()

# Main Streamlit app
def main():
    st.title("User Registration and Login")
    
    menu = ["Home", "Register", "Login"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Welcome to the User Management System")
        st.text("Select 'Register' to create a new account or 'Login' to access your account.")

    elif choice == "Register":
        st.subheader("Register a New User")
        with st.form("register_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Register")
        
        if submit:
            if password == confirm_password:
                register_user(name, email, password)
            else:
                st.error("Passwords do not match.")

    elif choice == "Login":
        st.subheader("Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

        if submit:
            user = login_user(email, password)
            if user:
                st.success(f"Welcome {user['name']}!")
                subprocess.run(["streamlit", "run", "new//cnvrted.py"])
                st.text("You are now logged in.")
                
            else:
                st.error("Invalid email or password.")

if __name__ == "__main__":
    initialize_database()  # Initialize database when app starts
    main()
