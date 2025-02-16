import streamlit as st
import mysql.connector


# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Shreya123456789",  # Change this
        database="DB_CREDIT"
    )


# Function to add user details
def add_user(aadhar_number, transaction_history, bills_paid_on_time, on_time_payments,
             utility_bill_payments, has_credit_card, credit_utilization, income_stability,
             debt_to_income_ratio, existing_loans, loans_paid, savings):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO admin_user_details (aadhar_number, transaction_history, bills_paid_on_time, on_time_payments, 
                                  utility_bill_payments, has_credit_card, credit_utilization, income_stability, 
                                  debt_to_income_ratio, existing_loans, loans_paid, savings) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (aadhar_number, transaction_history, bills_paid_on_time, on_time_payments,
             utility_bill_payments, has_credit_card, credit_utilization, income_stability,
             debt_to_income_ratio, existing_loans, loans_paid, savings)
        )
        conn.commit()
        st.success("User details added successfully!")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        conn.close()


# Streamlit UI - User Details Entry
def user_details_page():
    st.title("Enter User Details")

    aadhar_number = st.text_input("Aadhar Number")  # Aadhar is now the primary ID
    transaction_history = st.text_area("Transaction History")

    bills_paid_on_time = st.selectbox("Bills Paid on Time?", [1, 0])


    # Show "On-Time Payment Percentage" field only if "Yes" is selected, else set to 0
    if bills_paid_on_time == 1:
        on_time_payments = st.number_input("On-Time Payment Percentage", min_value=0, max_value=100, step=1)
    else:
        on_time_payments = 0  # Default to 0 if "No" is selected

    utility_bill_payments = st.number_input("Amount Paid for Utility Bills", min_value=0)

    # Checkbox for credit card ownership
    has_credit_card = st.checkbox("Does user have a credit card?")

    # Show credit utilization input only if the user has a credit card
    credit_utilization = 0
    if has_credit_card:
        credit_utilization = st.number_input("Credit Utilization (%)", min_value=0.0, max_value=100.0, format="%.2f")

    # Additional Fields
    income_stability = st.number_input("Income Stability (0.0 - 1.0)", min_value=0.0, max_value=1.0, format="%.2f")
    debt_to_income_ratio = st.number_input("Debt-to-Income Ratio (0.0 - 1.0)", min_value=0.0, max_value=1.0,
                                           format="%.2f")
    existing_loans = st.number_input("Number of Existing Loans", min_value=0, step=1)
    loans_paid = st.number_input("Number of Loans Paid", min_value=0, step=1)
    savings = st.number_input("Total Savings", min_value=0.0, format="%.2f")

    if st.button("Add User"):
        if aadhar_number and transaction_history:
            add_user(aadhar_number, transaction_history, bills_paid_on_time, on_time_payments,
                     utility_bill_payments, has_credit_card, credit_utilization, income_stability,
                     debt_to_income_ratio, existing_loans, loans_paid, savings)
        else:
            st.error("Aadhar Number and Transaction History are required fields!")


# Run the user details page
if __name__ == "__main__":
    user_details_page()
