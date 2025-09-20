from flask import Flask, render_template, request, redirect, url_for
import json
import re

from utils import get_available_cocktails

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def home():
    return redirect(url_for("cocktails"))

@app.route("/admin", methods = ["GET", "POST"])
def admin_panel():

    with open("data/stocks.json", encoding='utf-8') as f:
        stocks = json.loads(f.read())
    beers, ingredients = stocks["beers"], stocks["ingredients"]

    if request.method == "POST":
        # Update beers
        beerNames = request.form.getlist("beerName")
        beerTypes = request.form.getlist("beerType")
        beerDegrees = request.form.getlist("beerDegree")

        if len(beerNames) == len(beerTypes) and len(beerDegrees) == len(beerNames):
            beers = []
            for _ in range(len(beerNames)):
                beers.append({
                    "name": beerNames[_],
                    "type": beerTypes[_],
                    "degree": beerDegrees[_]
                })

        # Update ingredients
        ingredients = [i for i in request.form if request.form.get(i) == 'on']

        # Write data to file
        stocks = {
            "beers": beers,
            "ingredients": ingredients
        }

        with open("data/stocks.json", mode = "w", encoding = 'utf-8') as f:
            f.write(json.dumps(stocks))

    with open("data/ingredients.json", encoding='utf-8') as f:
        ingredients_list = json.loads(f.read())
    return render_template("admin.html", beers = beers, ingredients = ingredients, ingredients_list = ingredients_list)

@app.route("/beers", methods = ["GET"])
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

@app.route("/cocktails", methods = ["GET"])
def cocktails():
    # Get URL arguments
    cocktail_type: str = request.args.get("cocktail_type", default = "")
    ingredient_preferences: str = request.args.get("ingredient_preferences", default = "")

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

    return render_template("cocktails.html.jinja", page_title = "Cocktails", cocktails = available_cocktails, ingredients = available_ingredients)

@app.route("/others", methods = ["GET"])
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