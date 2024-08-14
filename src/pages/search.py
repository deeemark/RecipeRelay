import login as log
import requests as rq
from io import BytesIO
import streamlit as st
import pandas as pd

INTOLERANCES = [
    'Dairy', 'Egg', 'Gluten', 'Grain', 'Peanut', "Seafood", 'Seasame', 'Shellfish',
    'Soy', 'Sulfite', 'Tree Nut', 'Wheat']
CUISINES = [
    'African', 'Asian', 'American', 'British', 'Cajun', 'Caribbean', 'Chinese', 'Eastern European',
    'European', 'French', 'German', 'Greek', 'Indian', 'Irish', 'Italian', 'Japanese', 'Jewish',
    'Korean', 'Latin American', 'Mediterranean', 'Mexican', 'Middle Eastern', 'Nordic', 'Southern',
    'Spanish', 'Thai', 'Vietnamese']
DIETS = [
    'Gluten Free', 'Ketogenic', 'Vegetarian', 'Lacto-Vegetarian',
    'Ovo-Vegetarian', 'Vegan', 'Pescetarian', 'Paleo']
RECIPE_TYPES = [
    'main course', 'side dish', 'dessert', 'appetizer', 'salad', 'bread', 'breakfast',
    'soup', 'beverage', 'sauce', 'marinade', 'fingerfood', 'snack', 'drink']
API_KEY = "e994b422921547d0affd409cf45d4af2"

# initializing the session state variables
if "params" not in st.session_state:  # holds users ingredient list to be updated by the fragment
    st.session_state.params = {}
if "userN" not in st.session_state:  # to pass to our login module
    st.session_state.userN = ''
if "search" not in st.session_state:  # to pass to our login module
    st.session_state.search = True
if "successLogin" not in st.session_state:
    st.session_state.successLogin = False
if not st.session_state.successLogin:
    st.switch_page('main.py')

def addParameters(paramKey, paramValue, multi=False):
    """
    Takes a parameter key, parameter value and also a boolean that only passed so we know when to
    append if the value takes a list of strings.
    """
    if multi:
        (st.session_state.params).setdefault(paramKey, []).append(paramValue)
    else:
        st.session_state.params[paramKey] = paramValue

def get_image(url):
    """Takes a url for a image and returns the image to be displayed."""
    r = rq.get(url)
    return BytesIO(r.content)

@st.fragment
def recipeDisplay(response):
    """Takes a http response for the spoonacular api and disects it getting all the recipe info from it."""
    with st.container():
        widget_id = (id for id in range(1, 100_00))
        for items in response['results']:
            with st.expander(items['title']):

                st.image(get_image(items['image']))
                ir = rq.get(
                    f"""https://api.spoonacular.com/recipes/{items['id']}/information""",
                    params={'apiKey': API_KEY})
                iresponse = ir.json()
                st.write(iresponse['sourceUrl'])
                st.page_link(iresponse['sourceUrl'], label=items['title'])
                recipeIngredients = []
                yourIngredients = set(
                    (log.getIngredient(st.session_state.userN))[0])
                count = 0
                for items in iresponse['extendedIngredients']:
                    recipeIngredients.append(items['name'])
                for x in yourIngredients:
                    for y in recipeIngredients:
                        if x in y:
                            count += 1
                st.write(
                    f"""You are missing {len(recipeIngredients) - count} out of {len(recipeIngredients)}
                    ingredients from this recipe""")
                st.write(
                    "Would you like to add ingredients from this recipe to your grocery list?")
                ingredient_df = pd.DataFrame(
                    {
                        "Ingredients": recipeIngredients,
                        "Add": [False] * len(recipeIngredients)
                    }
                )
                updated = st.data_editor(
                    ingredient_df,
                    column_config={
                        "Add": st.column_config.CheckboxColumn(
                            "Add Ingredient to Your grocery list?",
                            default=False
                        )
                    },
                    disabled=["Ingredients"],
                    hide_index=True,
                )
                addToList = st.button(
                    'Add to grocery list', key=next(widget_id))
                if addToList:
                    toAdd = updated[updated['Add'] == True]
                    for x in toAdd['Ingredients'].tolist():
                        log.updateGrocery(x, st.session_state.userN)

                    st.write("succesfully added ingredients to grocery list")

@st.fragment
def displayParams(refresh=False):
    """
    Takes the Parameters list and displays them using streamlits write function if refresh is passed
    the fragment is rerun as to update the current display of parameters.
    """
    displayed = []
    if refresh:
        st.rerun()
    for para in st.session_state.params:
        if para == 'includeIngredients' or para == 'cuisine':
            for ingr in st.session_state.params[para]:
                ingrstatus = (f"Include {ingr}")
                if ingrstatus not in displayed:
                    st.write(ingrstatus)
                    displayed.append(ingrstatus)
        elif para == 'excludeIngredients' or para == 'excludeCuisine':
            for ingr in st.session_state.params[para]:
                ingrstatus = (f"Exclude {ingr}")
                if ingrstatus not in displayed:
                    st.write(ingrstatus)
                    displayed.append(ingrstatus)
        else:
            st.write(st.session_state.params[para])

# Navigation menu
st.sidebar.page_link("pages/user.py", label= "User Profile")
st.sidebar.page_link("pages/ingredients.py", label="Your ingredients list")
st.sidebar.page_link("pages/grocerylist.py", label="grocery list")
st.sidebar.page_link('main.py', label="Logout")

st.header("Recipe search")
st.write("Search the spoontacular database using a normal search or use advanced search to change the conditions")
query = st.text_input("enter your seach keywords")
search = st.button("search")
if search:
    r = rq.get(
        f"""https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&addRecipeinformation=true
        """, params=st.session_state.params)
    response = r.json()
    addParameters('query', query)
    if r.status_code in[401, 402, 403, 404]:
        st.write("Database currently unavailable")
    recipeDisplay(response)
with st.expander("Advanced search"):
    ingr = st.checkbox("Include/Exclude ingredients from ingredient list?")
    if ingr:
        on = st.radio("include or exclude", ['include', 'exclude'])
        options = st.multiselect(
            "choose from you Ingredient List", (log.getIngredient(st.session_state.userN))[0])
        ingrButton = st.button("Apply filter", key="ingredients")
        if ingrButton:
            if options and on == 'include':
                for items in options:
                    addParameters('includeIngredients', items, True)
            elif options and on == 'exclude':
                for items in options:
                    addParameters('excludeIngredients', items, True)

    cuisine = st.checkbox("Include/Exclude types of cuisinge?")
    if cuisine:
        on = st.radio("Include or exclude", ['include', 'exclude'])
        cuisineInclusion = st.selectbox("choose which cuisine", CUISINES)
        cuisineButton = st.button("Apply filter", key="cuisine")
        if cuisineButton:
            if cuisineInclusion and on == "include":
                addParameters('cuisine', cuisineInclusion, True)
            elif cuisineInclusion and on == "exclude":
                addParameters('excludeCuisine', cuisineInclusion, True)

    diet = st.checkbox("limit by diet?")
    if diet:
        dietlimit = st.selectbox("choose which diet", DIETS)
        dietButton = st.button('Apply filter', key='diet')
        if dietButton:
            if dietlimit:
                addParameters('diet', dietlimit)

    tolerences = st.checkbox("limit by intolerance?")
    if tolerences:
        toler = st.selectbox("choose which intolerance", INTOLERANCES)
        tolerancesButton = st.button('Apply filter', key='tolerance')
        if tolerancesButton:
            if toler:
                addParameters('intolerances', toler)

    recipeType = st.checkbox("Limit by recipe type?")
    if recipeType:
        recip = st.selectbox("choose which recipe type", RECIPE_TYPES)
        recipeButton = st.button('Apply filter', key='recipe')
        if recipeButton:
            if recip:
                addParameters('type', recip)
    displayParams()
    st.divider()

clearParams = st.button("clear filters?")
if clearParams:
    st.session_state.params = {}
    displayParams(True)
