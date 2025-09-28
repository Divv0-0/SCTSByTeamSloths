import streamlit as st

def run_login():
    st.title("Smart Classroom & Timetable Scheduler")
    st.subheader("Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        # In real case: validate against DB
        if user and pwd:
            st.session_state.logged_in = True
            st.session_state.username = user
            st.success("Login successful!")
        else:
            st.error("Please enter username & password")
