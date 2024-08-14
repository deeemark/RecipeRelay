import login as log
from collections import Counter
import streamlit as st
import pandas as pd

# initializing the session state variables
if "userN" not in st.session_state:
    st.session_state.userN = ''
if "updateList" not in st.session_state: 
    st.session_state.updateList = []
if "userList" not in st.session_state: 
    st.session_state.userList = []
if "successLogin" not in st.session_state:
    st.session_state.successLogin = False
#if not logged in
if not st.session_state.successLogin:
    st.switch_page('main.py')

@st.fragment
def ingredientlist():
    """Displays ingredients and allows you to add to, delete from, or reset the user specific igredient lis."""
    list = st.form("ingredient")
    ingr = list.selectbox(
        "Choose from the ingredients Below",
        df["Ingredient"].tolist(), placeholder="Choose an option")
    removeIngr = list.selectbox("Choose the ingredient you would like to remove", st.session_state.userList[0],
                                placeholder="Choose an option")

    submit = list.form_submit_button('add the ingredient')
    submit2 = list.form_submit_button('Remove An Element')
    submit3 = list.form_submit_button('Reset the List')
    if submit:
        log.updateIngredient(ingr, st.session_state.userN)
        st.rerun()
    if submit2:
        log.removeIngredient(st.session_state.userN, removeIngr)
        st.rerun()
    if submit3:
        log.resetIngredient(st.session_state.userN)
        st.rerun()
    st.session_state.userList = log.getIngredient(st.session_state.userN)
    st.write("Your ingredient list:")
    ingredientCount = Counter(st.session_state.userList[0])
    for x, y in ingredientCount.items():
        st.write(f'{x} x {y}')

# Navigation menu
st.sidebar.page_link("pages/user.py", label= "User Profile")
st.sidebar.page_link("pages/search.py", label="Search For a recipe")
st.sidebar.page_link("pages/grocerylist.py", label="grocery list")
st.sidebar.page_link("main.py", label="Logout")

# stores the top 1k ingredients and their IDs pulled from the spoontacular api
file_path = "src/top-1k-ingredients.csv"
df = pd.read_csv(file_path)

    
st.session_state.userList = log.getIngredient(st.session_state.userN)
st.session_state.updateList = pd.Series(
    st.session_state.userList[0], name="Ingredients")
st.title("Your Ingredient List")
st.write("Here you can enter what ingredients you have below")
st.write("Which can also be used to check against recipes ingredients and aid in your recipe searches")
st.divider()
ingredientlist()
