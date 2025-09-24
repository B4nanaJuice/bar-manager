from flask import Blueprint, render_template, request
import json

page = Blueprint("admin", __name__, template_folder = "templates", static_folder = "static")

@page.route("/admin", methods = ["GET", "POST"])
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