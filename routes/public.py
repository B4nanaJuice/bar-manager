from flask import Blueprint, redirect, url_for, render_template, request
import json
import re

from utils import get_available_cocktails

page = Blueprint("public", __name__, template_folder = "templates", static_folder = "static")

@page.route("/", methods = ["GET"])
def home():
    return redirect(url_for("public.cocktails"))

@page.route("/cocktails", methods = ["GET"])
def cocktails():
    # Get URL arguments
    cocktail_type: str = request.args.get("cocktail_type", default = "")
    ingredient_preferences: str = request.args.get("ingredient_preferences", default = "")
    mocktail: bool = request.args.get("no_alcohol", default = False) != False

    # Get ingredients stock
    with open("data/stocks.json", encoding='utf-8') as f:
        stocks = json.loads(f.read())
        available_ingredients = stocks["ingredients"]

    # Get available cocktails
    available_cocktails: list[dict] = get_available_cocktails(available_ingredients)

    # Sort available cocktails if URL arguments
    if cocktail_type != "":
        available_cocktails = [_ for _ in available_cocktails if _["type"] == cocktail_type]

    if ingredient_preferences != "":
        ingredient_preferences: list[str] = ingredient_preferences.split(",")
        # Variable matches = list of tuples having : 
        # - in first place the cocktail itself
        # - in second place the number of matches between the ingredients of the cocktail and the ingredient_preferences
        matches: list[tuple] = [
                (_c, len([_ for _ in [i["name"] for i in _c["ingredients"]] if _.lower() in [i.lower() for i in ingredient_preferences]]))
                for _c in available_cocktails
            ]
        # Sort the mateches variable by number of matches
        matches = sorted(matches, key = lambda t: t[1], reverse = True)
        # Take only entries with at least 1 match
        matches = [_ for _ in matches if _[1] >= 1]

        available_cocktails = [_[0] for _ in matches]

    if mocktail:
        available_cocktails = [_ for _ in available_cocktails if _["has_alcohol"] == False]

    return render_template("cocktails.html.jinja", page_title = "Cocktails", cocktails = available_cocktails, ingredients = available_ingredients)

@page.route("/beers", methods = ["GET"])
def beers():
    # Get URL arguments
    beer_type: str = request.args.get("beer_type", default = "")

    # Get information for json file
    with open("data/stocks.json", encoding='utf-8') as f:
        stocks = json.loads(f.read())

    # Filter data from beer type (if there is a specified type)
    if beer_type == "":
        beers = stocks["beers"]
    else:
        beers: list = [b for b in stocks["beers"] if b["type"] == beer_type]

    # Render the template with the wanted beers
    return render_template("beers.html.jinja", page_title = "Bières", beers = beers)

@page.route("/others", methods = ["GET"])
def others():
    # Get the stocks
    with open("data/stocks.json", encoding='utf-8') as f:
        stocks = json.loads(f.read())

    # Filter to get only juices and syrups
    ingredients: list[str] = stocks["ingredients"]
    juices: list[str] = [_ for _ in ingredients if re.match(r"^Jus", _)]
    syrups: list[str] = [_ for _ in ingredients if re.match(r"^Sirop", _)]

    # Render the template
    return render_template("others.html.jinja", page_title = "Autres", juices = juices, syrups = syrups)