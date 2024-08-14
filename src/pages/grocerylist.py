import streamlit as st
import login as log
from collections import Counter

# initializing the session state variables
if "userN" not in st.session_state: 
    st.session_state.userN = ''
if "successLogin" not in st.session_state:
    st.session_state.successLogin = False
if not st.session_state.successLogin:
    st.switch_page('main.py') 

@st.fragment
def displayGrocery():
    """Displays user specific grocery and allows you to remove from or reset list."""
    groceryList = (log.getGrocery(st.session_state.userN))[0]
    with st.container():
        st.header("Ingredients")
        st.divider()
        ingredientCount = Counter(groceryList)
        if groceryList == None:
            st.write("Empty List")
        for x, y in ingredientCount.items():
            st.write(f'{x} x {y}')
    with st.expander("edit list"):
        removeItem = st.selectbox("Do you want to remove a Grocery list item", groceryList,
                                    placeholder="Choose an option")
        submit2 = st.button('Remove An Item')
        submit3 = st.button('Reset the List')
        if submit2:
            log.removeGrocery(removeItem, st.session_state.userN)
            st.rerun()
        if submit3:
            log.resetGrocery(st.session_state.userN)
            st.rerun()    

# Navigation menu
st.sidebar.page_link("pages/user.py", label= "User Profile")
st.sidebar.page_link("pages/search.py", label="Search For a recipe")
st.sidebar.page_link("pages/ingredients.py", label="Your ingredients list")
st.sidebar.page_link('main.py', label="Logout")

st.title("Your Grocery List")
displayGrocery()