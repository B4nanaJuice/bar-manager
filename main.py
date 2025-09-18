from flask import Flask, render_template, request, redirect, url_for
import json
import re

app = Flask(__name__)

def get_available_cocktails(available_ingredients: list) -> list:
    with open("data/cocktails.json", encoding='utf-8') as f:
        cocktails: list = json.loads(f.read())

    available_cocktails: list = []
    for cocktail in cocktails:
        cocktail_ingredients = [ingredient["name"] for ingredient in cocktail["ingredients"]]
        if len(list(set(cocktail_ingredients) - set(available_ingredients))) == 0:
            available_cocktails.append(cocktail)

    return available_cocktails

# @app.route("/", methods = ["GET"])
# def home():
#     with open("data/stocks.json", encoding='utf-8') as f:
#         stocks = json.loads(f.read())
#     beers: list = stocks["beers"]
#     cocktails: list = get_available_cocktails(stocks["ingredients"])
#     return render_template("home.html", beers = beers, cocktails = cocktails)

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
    return render_template("beers.html.jinja", beers = beers)

@app.route("/cocktails", methods = ["GET", "POST"])
def cocktails():
    if request.method == "POST":
        pass

    cocktails = []
    return render_template("cocktails.html", cocktails = cocktails)

@app.route("/others", methods = ["GET"])
def others():
    # Get the stocks
    with open("data/stocks.json", encoding='utf-8') as f:
        stocks = json.loads(f.read())

    # Filter to get only juices and syrups
    ingredients: list[str] = stocks["ingredients"]
    juices: list[str] = [_ for _ in ingredients if re.match(r"^Jus", _)]
    syrups: list[str] = [_ for _ in ingredients if re.match(r"^Sirop", _)]
    return render_template("others.html", juices = juices, syrups = syrups)