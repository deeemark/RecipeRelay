# _Recipe Relay_

Recipe Relay is a streamlit based web app that allows to user to input ingredients and
use those to search for compatible recipes from which you can add ingredients to a grocery list.

![alt text](Recipe_Relay.png)

## Key Features

- Create a list of ingredients you have around
- Use those ingredient or many other filters to search for recipes
- Able to add thos recipe ingredients to a grocery list
- Able to edit that grocery list

## Tech

Recipe relay uses a few technologies:

- [Pandas]
- [Streamlit]
- [PosgreSQL]
- [Psycopg2]
- [Requests]

## Installation

Recipe Relay requires a postgresql server to run
first set the database.ini file to your database
then Install the dependencies from the toml file.

```sh
python -m pip install .
```

And run the StreamLit web app by

```sh
streamlit run src\main.py
```

## API

Recipe Relay uses spoonacular web api to pull recipes and various other info from https://spoonacular.com/food-api

## Development

This a mostly just a fun practice project for myself so dont contribute lol, but if you do want to use it as a reference or a base knock your self out

## License

MIT
