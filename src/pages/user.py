import streamlit as st

# initializing the session state variables
if "userN" not in st.session_state:  
    st.session_state.userN = ''
if "successLogin" not in st.session_state:
    st.session_state.successLogin = False
if not st.session_state.successLogin:
    st.switch_page('main.py')   
# Navigation menu
st.sidebar.page_link("pages/search.py", label= "Search For a recipe")
st.sidebar.page_link("pages/ingredients.py", label= "Your ingredients list")
st.sidebar.page_link("pages/grocerylist.py", label="grocery list")
st.sidebar.page_link('main.py', label= "Logout")
st.title(f"Hello {st.session_state.userN}!!!")
st.text("What would you like to do today?")
