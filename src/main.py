import login as log
import pandas as pd
import streamlit as st
import psycopg2

if "userN" not in st.session_state:
    st.session_state.userN = ''
if "passW" not in st.session_state:
    st.session_state.passW = ''
if "successLogin" not in st.session_state:
    st.session_state.successLogin = False

@st.fragment
def login():
    """Contains both the expander container for both the login and the create and account function"""
    with st.expander("Login"):
        with st.form("Login"):
            username = st.text_input('input your username')
            password = st.text_input('input your password')
            st.session_state.userN = username
            st.session_state.passW = password
            submit = st.form_submit_button('Login')
        correct = log.login(st.session_state.userN, st.session_state.passW)
        if submit:
            if correct:
                st.write("Username = ", st.session_state.userN)
                st.write("Password = ", st.session_state.passW)
                st.session_state.successLogin = True
                st.write("Login successful")
                st.switch_page("pages/user.py")
            else:
                st.write("login failed")
                st.session_state.successLogin = "Login Failed"
    with st.expander("Create account"):
        with st.form("Create account"):
            st.write("""Create a unique username and a password with atleat 8 characters and less than 30""")
            st.write("atleast one digit")
            st.write("atleast one special symbol")
            st.write("and atleast one digit.")
                
                
            username = st.text_input('input your username')
            password = st.text_input('input your password')
            st.session_state.userN = username
            st.session_state.passW = password
            create = st.form_submit_button("create")
            if create:
                success = log.createAccount(username, password)
                if success[0]:
                    st.write('account successfully created')
                else:
                    st.write(f"account creation failed: {success[1]} invalid")
log.createDatabase()
st.title('Login')
login()
