import streamlit as st
import login
import main

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    main.run_main()
else:
    login.run_login()
