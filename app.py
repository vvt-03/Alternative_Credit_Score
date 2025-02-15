import streamlit as st
import pickle
import pandas as pd

# Load trained model
with open("credit_score_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("Credit Score Predictor")

# User inputs
st.sidebar.header("Enter details")

def user_input():
    data = {
        "Transaction History": st.sidebar.number_input("Transaction History", value=5000),
        "On-time Payments (%)": st.sidebar.slider("On-time Payments (%)", 0, 100, 80),
        "Income Stability": st.sidebar.number_input("Income Stability", value=0.5),
        "Debt-to-Income Ratio": st.sidebar.number_input("Debt-to-Income Ratio", value=0.3),
        "Credit Utilization (%)": st.sidebar.slider("Credit Utilization (%)", 0, 100, 30),
        "Existing Loans": st.sidebar.number_input("Existing Loans", value=2),
        "Loan Repayment History": st.sidebar.number_input("Loan Repayment History", value=1),
        "Salary": st.sidebar.number_input("Salary", value=50000),
        "Savings": st.sidebar.number_input("Savings", value=100000),
        "Employment Type": st.sidebar.selectbox("Employment Type", ["Salaried", "Self-employed"]),
        "Bills Paid on Time": st.sidebar.selectbox("Bills Paid on Time", ["Yes", "No"]),
        "Social Media Engagement": st.sidebar.number_input("Social Media Engagement", value=5000),
        "Utility Bill Payments": st.sidebar.number_input("Utility Bill Payments", value=2000),
        "Gender": st.sidebar.selectbox("Gender", ["Male", "Female"]),
        "City": st.sidebar.selectbox("City", ["Bangalore", "Delhi", "Hyderabad"]),
        "Income Variability": st.sidebar.selectbox("Income Variability", ["High", "Low"]),
        "Age": st.sidebar.number_input("Age", value=30)
    }
    return pd.DataFrame([data])

df = user_input()

if st.button("Predict Credit Score"):
    prediction = model.predict(df)[0]
    st.subheader(f"Predicted Credit Score: {prediction:.2f}")