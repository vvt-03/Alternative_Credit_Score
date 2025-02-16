import streamlit as st
import mysql.connector

# ----------------- Database Connection -----------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Shreya123456789",  # Replace with your MySQL password
        database="DB_CREDIT"
    )

# ----------------- Insert User Details into Database -----------------
def register_user_details(email, age, aadhar_number, gender, city, marketing_expense, employment_type, monthly_earning):
    """Inserts the user details into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO user_details (email, aadhar_number, age, gender, city, marketing_expense, employment_type, salary)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (email, aadhar_number, age, gender, city, marketing_expense, employment_type, monthly_earning))

        conn.commit()
        st.success("✅ Profile completed successfully! Redirecting...")
        st.switch_page("home.py")  # Redirect to home/dashboard

    except mysql.connector.Error as err:
        st.error(f"❌ Database Error: {err}")
    finally:
        cursor.close()
        conn.close()

# ----------------- Streamlit UI -----------------
st.title("📝 Complete Your Profile")

email = st.text_input("📧 Email")
age = st.number_input("🎂 Age", min_value=18, max_value=100, step=1)
aadhar_number = st.text_input("🆔 Aadhar Number (Stored as plain text)")
gender = st.selectbox("⚧️ Gender", ["Male", "Female", "Other"])
city = st.text_input("🏙️ City")
marketing_expense = st.number_input("📊 Marketing Expense (₹)", min_value=0.0, format="%.2f")

employment_type = st.selectbox("💼 Employment Status", ["Salaried", "Self-Employed", "Unemployed"])
monthly_earning = 0.0
if employment_type in ["Salaried", "Self-Employed"]:
    monthly_earning = st.number_input("💰 Monthly Earning (₹)", min_value=0.0, format="%.2f")

# ----------------- Submit Button -----------------
if st.button("Submit"):
    if not email or not aadhar_number or not age or not city:
        st.error("⚠️ Please fill in all required fields.")
    else:
        register_user_details(email, age, aadhar_number, gender, city, marketing_expense, employment_type, monthly_earning)
        st.success("Profile successfully created..Please login")
