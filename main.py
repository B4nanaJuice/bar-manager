from flask import Flask, render_template, request
import json

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

@app.route("/", methods = ["GET"])
def home():
    with open("data/stocks.json", encoding='utf-8') as f:
        stocks = json.loads(f.read())
    beers: list = stocks["beers"]
    cocktails: list = get_available_cocktails(stocks["ingredients"])
    return render_template("home.html", beers = beers, cocktails = cocktails)

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