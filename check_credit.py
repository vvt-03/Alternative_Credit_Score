import os

import streamlit as st
import pickle
import pandas as pd
import mysql.connector
import plotly.express as px
import numpy as np
import datetime

# Check if the user is logged in
if "user_logged_in" not in st.session_state or not st.session_state.user_logged_in:
    st.warning("🚫 You must log in to access this page.")
    st.stop()  # Stop execution if not logged in

# Proceed to load model and predict credit score if logged in
try:
    with open("credit_score_model.pkl", "rb") as f:
        model = pickle.load(f)
    st.write("✅ Model Loaded Successfully!")
except Exception as e:
    st.error(f"❌ Error loading model: {e}")
    st.stop()  # Stop execution if model fails to load

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Shreya123456789",
        database="DB_CREDIT"
    )

# Fetch user details from database using Aadhar number
def get_user_data(aadhar_number):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_details WHERE aadhar_number = %s", (aadhar_number,))
    user_data = cursor.fetchone()

    cursor.execute("SELECT * FROM admin_user_details WHERE aadhar_number = %s", (aadhar_number,))
    admin_data = cursor.fetchone()

    conn.close()
    return user_data, admin_data

st.title("📊 Credit Score Predictor")
st.sidebar.header("Select User")

# User enters Aadhar Number
aadhar_number = st.sidebar.text_input("Enter Aadhar Number", max_chars=12)
if "user_data" not in st.session_state:
    st.session_state.user_data = None
if "admin_data" not in st.session_state:
    st.session_state.admin_data = None

if st.sidebar.button("Fetch Data"):
    user_data, admin_data = get_user_data(aadhar_number)

    if user_data and admin_data:
        st.session_state.user_data = user_data
        st.session_state.admin_data = admin_data
        st.success("✅ User Data Retrieved Successfully!")

if st.session_state.user_data and st.session_state.admin_data:
    user_data = st.session_state.user_data
    admin_data = st.session_state.admin_data

    # Convert categorical and boolean values to numeric
    bills_paid_on_time = str(admin_data["bills_paid_on_time"])
    has_credit_card = 1 if admin_data["has_credit_card"] else 0
    income_variability = "Yes"
        # Create DataFrame for model prediction
    df = pd.DataFrame([{
            "Transaction History": admin_data["transaction_history"],
            "On-time Payments (%)": admin_data["on_time_payments"],
            "Income Stability": admin_data["income_stability"],
            "Income Variability": income_variability,
            "Debt-to-Income Ratio": admin_data["debt_to_income_ratio"],
            "Credit Utilization (%)": admin_data["credit_utilization"],
            "Existing Loans": admin_data["existing_loans"],
            "Loan Repayment History": admin_data["loan_repayment_history"],
            "Loans Paid": admin_data["loans_paid"],
            "Salary": user_data["salary"],
            "Savings": admin_data["savings"],
            "marketing": user_data["marketing_expense"],
            "Utility Bill Payments": admin_data["utility_bill_payments"],
            "Age": user_data["age"],
            "Gender": user_data["gender"],
            "City": user_data["city"],
            "Employment Type":user_data["employment_type"],
            "Bills Paid on Time": bills_paid_on_time,
            "Has Credit Card": has_credit_card
        }])
        # Display input data before prediction
    st.write("📊 Input Data for Prediction:")
    st.write(df)
    if df.isnull().values.any():
        st.error("⚠ Data contains NULL values! Please check inputs.")

    if st.button("🔍 Predict Credit Score"):
        prediction = model.predict(df)[0]
        st.subheader(f" Predicted Credit Score: {prediction:.2f}")
        st.write(prediction)

        # Assign Bank & Interest Rate
        if prediction >= 750:
            bank = "🏦 Bank A"
            interest_rate = "7.5% - 8.5% (Lowest interest)"
            st.success("🟢 Excellent Credit Score! You qualify for the best interest rates.")
        elif prediction >= 650:
            bank = "🏦 Bank B"
            interest_rate = "9.0% - 11.0% (Moderate interest)"
            st.info("🟡 Good Credit Score! You qualify for moderate interest rates.")
        else:
            bank = "🏦 Bank C"
            interest_rate = "12.5% - 15.0% (High interest)"
            st.warning("🔴 Poor Credit Score. You qualify for a higher interest rate.")

        # Display Bank & Interest Rate Details
        st.write(f"✅ Assigned Bank: {bank}")
        st.write(f"💰 Interest Rate: {interest_rate}")

        # Pie Chart Visualization
        st.subheader("📊 Financial Overview")

        pie_data = {
            "Transaction History": df["Transaction History"][0],
            "On-time Payments": df["On-time Payments (%)"][0],
            "Income Stability": df["Income Stability"][0],
            "Debt-to-Income Ratio": df["Debt-to-Income Ratio"][0],
            "Credit Utilization": df["Credit Utilization (%)"][0],
            "Existing Loans": df["Existing Loans"][0],
            "Loan Repayment History": df["Loan Repayment History"][0],
            "Salary": df["Salary"][0],
            "Savings": df["Savings"][0],
            "marketing": df["marketing"][0],
            "Utility Bill Payments": df["Utility Bill Payments"][0],
            "Age": df["Age"][0]
        }

        pie_df = pd.DataFrame({
            "Category": pie_data.keys(),
            "Value": pie_data.values()
        })

        fig = px.pie(
            pie_df,
            names="Category",
            values="Value",
            title="📊 Financial Overview",
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.3
        )

        st.plotly_chart(fig)

        # Simulate Monthly Credit Score Variation
        def generate_monthly_credit_scores(current_score, months=12):
            # Simulate variations: Random small changes (increase/decrease of up to ±5%)
            variation = np.random.uniform(-0.05, 0.05, months - 1)
            historical_scores = [current_score * (1 + variation[i]) for i in range(months - 1)]
            historical_scores.append(current_score)  # Add current month's score at the end
            return historical_scores

        if st.button("📈 Show Credit Score Trend"):
            try:
                # Simulate historical data based on predicted credit score
                current_score = prediction
                months = 12  # Show data for the last 12 months
                monthly_scores = generate_monthly_credit_scores(current_score, months=months)

                # Create a list of month labels
                month_labels = [(datetime.datetime.now() - datetime.timedelta(days=30 * i)).strftime("%b %Y") for i in range(months)]
                month_labels.reverse()  # Ensure chronological order

                # Create a DataFrame for visualization
                trend_df = pd.DataFrame({
                    "Month": month_labels,
                    "Credit Score": monthly_scores
                })

                # Plot the line graph
                st.subheader("📊 Monthly Credit Score Trend")
                fig = px.line(
                    trend_df,
                    x="Month",
                    y="Credit Score",
                    title="Monthly Credit Score Trend",
                    markers=True,
                    line_shape="spline",
                    color_discrete_sequence=["#1f77b4"]
                )

                st.plotly_chart(fig)
            except Exception as e:
                st.error(f"❌ Error generating credit score trend: {e}")
            else:
                st.error("⚠ No user data found! Please enter a valid Aadhar Number.")