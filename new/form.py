import streamlit as st
import pymysql

# Database connection setup
def create_connection():
    return pymysql.connect(
        host="localhost",      # Change to your database host
        user="root",           # Change to your database username
        password="Sudarshan@SQL",           # Change to your database password
        database="user_management",  # Change to your database name
        cursorclass=pymysql.cursors.DictCursor
    )

# Function to register a new user
def register_user(name, email, password):
    try:
        conn = create_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, password)
            )
        conn.commit()
        st.success("User registered successfully!")
    except pymysql.MySQLError as e:
        st.error(f"Error: {e}")
    finally:
        conn.close()

# Function to validate user login
def login_user(email, password):
    try:
        conn = create_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE email = %s AND password = %s",
                (email, password)
            )
            user = cursor.fetchone()
        return user
    except pymysql.MySQLError as e:
        st.error(f"Error: {e}")
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
                st.text("You are now logged in.")
            else:
                st.error("Invalid email or password.")

if __name__ == "__main__":
    main()
