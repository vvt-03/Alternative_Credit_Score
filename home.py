import streamlit as st

# Set page title
st.set_page_config(page_title="CrediFlow", page_icon="💰", layout="centered")

# Title
st.title("CrediFlow")
st.subheader("Welcome to CrediFlow - Your Banking Solution")

# Navigation Buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("User Login"):
        st.switch_page("pages/user_signup.py")

with col2:
    if st.button("User Signup"):
        st.switch_page("pages/user_signup.py")

with col3:
    if st.button("Dashboard (App)"):
        st.switch_page("pages/admin_login.py")

# Footer
st.markdown("---")
st.caption("© 2025 CrediFlow. All rights reserved.")
