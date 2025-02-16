import streamlit as st
import mysql.connector
import hashlib

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Shreya123456789",
        database="DB_CREDIT"
    )
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to verify user login
def authenticate_user(email, password_hash):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM user_auth WHERE email = %s AND password_hash = %s"
    cursor.execute(query, (email, password_hash))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user


st.title("🔐 User Login")

email = st.text_input("📧 Email")
password = st.text_input("🔑 Password", type="password")
password_hash = hash_password(password)
if st.button("Login"):
    user = authenticate_user(email, password_hash)

    if user:
        st.session_state.user_logged_in = True  # ✅ Store login status
        st.session_state.user_email = email  # Optional: Store user email
        st.success("✅ Login successful! Redirecting...")
        st.switch_page("pages/check_credit.py")  # Redirect to main page
    else:
        st.error("❌ Invalid email or password.")
