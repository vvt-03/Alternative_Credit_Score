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


# Function to check if user already exists
def user_exists(email):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT email FROM user_auth WHERE email = %s", (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user is not None  # Returns True if email exists


# Function to insert user data into MySQL
def register_user(name, email, password):
    if user_exists(email):
        st.warning("⚠️ Email already registered! Please log in instead.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO user_auth (name, email, password_hash)
            VALUES (%s, %s, %s)
        """, (name, email, hash_password(password)))

        conn.commit()

        # Store user email in session state and redirect to "More About You"
        st.session_state["new_user_email"] = email
        st.success("✅ User registered successfully! Redirecting to more details...")
        st.rerun()  # Rerun the app to apply session changes

    except mysql.connector.Error as err:
        st.error(f"❌ Error: {err}")
    finally:
        cursor.close()
        conn.close()


# Streamlit UI
st.title("📝 User Signup")

name = st.text_input("👤 Full Name")
email = st.text_input("📧 Email")
password = st.text_input("🔑 Password", type="password")

if st.button("Sign Up"):
    if name and email and password:
        register_user(name, email, password)
    else:
        st.error("⚠️ Please fill in all fields.")

# Redirect to "More About You" if a new user just signed up
if "new_user_email" in st.session_state:
    st.switch_page("pages/more_about_you.py")  # Redirect to additional details page

# Redirect to login if user is already registered
st.page_link("pages/user_login.py", label="🔑 Already have an account? Login here", icon="🔑")