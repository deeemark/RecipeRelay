from config import load_config
import psycopg2

# ==================================================================================================================================
def createAccount(username, password):
    """Facilitates account creation through validation checking the passed
    username and password, and uses those to fill out a database row for that users account
    returns boolean passed on if the creation was successful and if it wasnt returns the cause.

    Parameters:
    username(string): chosen user name for the account
    password(string): chosen password for the account
    Returns:
    list: a 2 element list with a boolean stored in the first index and what failed it if applicable
    stored in the second
    """
    conn, curr = openDatabase()
    usernameValid = usernameValidation(username)
    if not usernameValid:
        return [False, "Username"]

    valid = passwordValidation(password)
    if not valid:
        return [False, "Password"]
    placeHolderEmail = username + password + "@based.org"
    curr.execute(
        f"""INSERT INTO user_info(username, password, email, created_at, last_accessed)
        VALUES('{username}', '{password}', '{placeHolderEmail}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"""
        )
    curr.execute(f"SELECT user_id from user_info where username = '{username}'")
    curr.execute(
            f"""insert into user_ingredient_info(user_id) VALUES('{curr.fetchone()[0]}')""")
    conn.commit()
    closeDatabase(conn, curr)
    return [True,""]

# ================================================================================================================================
def passwordValidation(password):
    """Runs password through validation checks and returns a boolean."""
    if len(password) < 8 or len(password) > 30:
        print("password is not an valid length")
        return False
    if not any(char.isdigit() for char in password):
        print("Please input one or more digits in your password")
        return False
    if not any(char.isupper() for char in password):
        print("make sure to use atleast 1 uppercase letter in your password")
        return False
    if not any(char in ["$", "@", "#", "%"] for char in password):
        print("please make sure to use atleast special character in your password")
        return False
    print("Your password is valid")
    return True

# ==================================================================================================================================
def usernameValidation(useName):
    """Validates if a username is unique in the database."""
    conn, curr = openDatabase()
    try:
        curr.execute(
            f"SELECT username from user_info where username = '{useName}'")
        exists = curr.fetchone()
        closeDatabase(conn, curr)
        if exists:
            return False
        else:
            return True

    except (psycopg2.DatabaseError, Exception) as error: #database wasnt able to be acessed
        print(error)

# ==================================================================================================================================
def openDatabase():
    """Opens a connection with a database and returns the database and cursor object."""
    config = load_config()      #  loads default database login information from config
    conn = psycopg2.connect(**config)
    curr = conn.cursor()
    return [conn, curr]

# ==================================================================================================================================
def closeDatabase(conn, curr):
    """Closes passed database objects"""
    conn.close()
    curr.close()

# ============================================================================================================================++
def createDatabase():
    """Creates a default layout for the database and returns a boolean if successful."""
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            print("Connected to the PostgreSQL sever")
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS user_info(
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(50) NOT NULL,
                email VARCHAR(255) unique NOT NULL,
                created_at TIMESTAMP NOT NULL,
                last_accessed TIMESTAMP NOT NULL
                )
                """)
            cur.execute("""CREATE TABLE IF NOT EXISTS admin_info(
                user_id int PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                level int  NOT NULL
                )
                """)
            cur.execute("""CREATE TABLE IF NOT EXISTS user_ingredient_info(
                user_id int PRIMARY KEY,
                ingredient_info TEXT [],
                grocery_info TEXT []
                )
                """)

            return True

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return False

# ================================================================================================================================
def login(username, password):
    """Takes username and password and validates them and returns boolean if successful or not.
    TOD: implent another table to union and check admin status
    """
    conn, curr = openDatabase()
    userExists = usernameValidation(username)
    if not userExists:
        curr.execute(
            f"select password from user_info where username = '{username}'")
        if password == curr.fetchone()[0]:
            closeDatabase(conn, curr)
            return True
    closeDatabase(conn, curr)
    return False

# ==================================================================================================================================
def updateIngredient(item, username):
    """Adds passed item into user_ingredient_info table under the ingredient_info column."""
    conn, curr = openDatabase()
    curr.execute(f"""update user_ingredient_info
                     SET ingredient_info = ARRAY_APPEND(ingredient_info, '{item}')
                     where user_id = (SELECT user_id FROM user_info WHERE username ='{username}')
                 """)
    conn.commit()
    closeDatabase(conn, curr)

# =============================================================================================================================
def getIngredient(username):
    """returns the ingredient_info_info column associated with the username."""
    conn, curr = openDatabase()
    curr.execute(f"""SELECT ingredient_info from user_ingredient_info 
                 where user_id = (SELECT user_id FROM user_info WHERE username ='{username}')""")
    res = curr.fetchone()
    closeDatabase(conn, curr)
    return res

# ==================================================================================================================================
def resetIngredient(username):
    """Resets the ingredient_info column of the user_ingredient_info array to None."""
    conn, curr = openDatabase()
    curr.execute(f"""update user_ingredient_info 
                 set ingredient_info = Null 
                 where user_id = (SELECT user_id FROM user_info WHERE username ='{username}')""")
    conn.commit()
    closeDatabase(conn, curr)

# ==================================================================================================================================
def removeIngredient(username, ingredient):
    """Removes the passed ingredient from the ingredient_info column."""
    conn, curr = openDatabase()
    curr.execute(f"""
                UPDATE user_ingredient_info
                SET ingredient_info = ARRAY_REMOVE(ingredient_info, '{ingredient}')
                WHERE user_id = (SELECT user_id FROM user_info WHERE username ='{username}')
                 """)
    conn.commit()
    closeDatabase(conn, curr)

# ==================================================================================================================================
def updateGrocery(ingredient, username):
    """Adds passed ingredient to grocery_info column under in the user_ingerdient_info table."""
    conn, curr = openDatabase()
    curr.execute(f"""update user_ingredient_info
                     SET grocery_info = ARRAY_APPEND(grocery_info, '{ingredient}')
                     where user_id = (SELECT user_id FROM user_info WHERE username ='{username}')
                 """)
    conn.commit()
    closeDatabase(conn, curr)

# =============================================================================================================================
def getGrocery(username):
    """Returns the grocery_info column of the user_ingredient_info tabl.e"""
    conn, curr = openDatabase()
    curr.execute(f"""SELECT grocery_info from user_ingredient_info 
                 where user_id = (SELECT user_id FROM user_info WHERE username ='{username}')""")
    res = curr.fetchone()
    closeDatabase(conn, curr)
    return res

# ==================================================================================================================================
def resetGrocery(username):
    """Resets the grocery_info  column None."""
    conn, curr = openDatabase()
    curr.execute(f"""update user_ingredient_info 
                 set grocery_info = Null 
                 where user_id = (SELECT user_id FROM user_info WHERE username ='{username}')""")
    conn.commit()
    closeDatabase(conn, curr)

# ==================================================================================================================================
def removeGrocery(ingredient, username):
    """removes ingredient out of associated grocery info column"""
    conn, curr = openDatabase()
    curr.execute(f"""
                UPDATE user_ingredient_info
                SET grocery_info = ARRAY_REMOVE(grocery_info, '{ingredient}')
                WHERE user_id = (SELECT user_id FROM user_info WHERE username ='{username}')
                 """)
    conn.commit()
    closeDatabase(conn, curr)
# ==================================================================================================================================

if __name__ == "__main__":
    pass
