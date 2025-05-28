# Chat GPT wurde als Hilfsmittel für Teile des vorliegenden Codes benutzt. Dies ist mit einem (*) gekennzeichnet.

# Import der erforderlichen pip packages
import os
import streamlit as st
import pandas as pd
import requests

# Lesen vom Spoonacular API Key aus einer Umgebungsvariable (Security)
API_KEY = os.getenv("API_KEY")
# Definition der API Base URL
API_BASE_URL = "https://api.spoonacular.com"

# Globale Variable für die Rezepte
recipes_data = []

def get_recipes(ingredients: str) -> None:
    """Ruft Rezepte von der Spoonacular API ab.

    Args:
        ingredients: Kommagetrennte Zutaten als String
    """
    global recipes_data
    recipes_data = []

    # Aufbereitung der Zutaten als URL Parameter für den API Aufruf
    ingredient_list = ingredients.split(',')
    ingredients_url_parameters = ',+'.join([i.strip() for i in ingredient_list])
    
    # Rezepte von der 'findByIngredients' API abrufen (*)
    response = requests.get(
        f"{API_BASE_URL}/recipes/findByIngredients",
        params={
            "apiKey": API_KEY,
            "ingredients": ingredients_url_parameters
        }
    )

    if response.status_code == 200:
        recipes_data = response.json()
    else:
        try:
            error_message = response.json().get("message", "Unknown error")
        except Exception:
            error_message = "Unknown error"
        recipes_data = f"API error {response.status_code}: {error_message}"


def format_amount_number(amount: float) -> str:
    """Rundet eine Gleitzahl auf zwei Dezimalstellen und gibt sie als String zurück"""
    amount = round(amount, 2)
    if amount == int(amount):
        return str(int(amount))
    else:
        return str(amount)


def create_ingredients_dataframe(people_count: int, recipe: dict) -> pd.DataFrame:
    """Erstellt ein Dataframe für ein Rezept und die Personenanzahl"""
    data = {}

    for ingredient in recipe["usedIngredients"]:
        name = ingredient['originalName']
        data[name] = people_count * ingredient['amount']

    for ingredient in recipe["missedIngredients"]:
        name = ingredient['originalName']
        data[name] = people_count * ingredient['amount']

    df = pd.DataFrame.from_dict(data, orient='index')
    df.rename(columns={0: 'Amount'}, inplace=True)
    df.index.name = 'Ingredient'
    return df


# Erstellung der Webapplikation
st.set_page_config(page_title="Recipe Finder", page_icon="🍽️")
st.title("Recipe Finder")
st.write("""Discover delicious recipes based on the ingredients you have on hand!
Simply enter your ingredients and find suitable recipes for your next meal.""")

# Eingabefelder für die Anzahl der Personen und Zutaten
st.subheader("Input Ingredients separated by comma")
people_count = st.number_input("Number of people", min_value=1, max_value=100, step=1, value=1)
ingredients = st.text_input("Ingredients", placeholder="Flour, eggs, ...")

# Button zum Abrufen de

