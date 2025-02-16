import streamlit as st
import mysql.connector
import hashlib

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Shreya123456789",  # Replace with your MySQL password
        database="DB_CREDIT"
    )

# Hash password function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Admin authentication
def authenticate_admin(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
    admin = cursor.fetchone()

    conn.close()

    if admin and admin["password_hash"] == hash_password(password):
        return True
    return False

# Streamlit UI
st.title("Admin Login")

# Session management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_admin(username, password):
            st.session_state.logged_in = True
            st.success("Login successful! 🎉")
            st.rerun()  # ✅ Refresh page to show admin dashboard
        else:
            st.error("Invalid credentials. Please try again.")

# Display admin dashboard after login
if st.session_state.logged_in:
    st.subheader("Welcome, Admin!")
    st.write("Here you can manage user details and view data.")

    # Add buttons or links to navigate within the app
    if st.button("Enter User Details"):
        st.switch_page("pages/user_details.py")


    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False, "username": None}))
