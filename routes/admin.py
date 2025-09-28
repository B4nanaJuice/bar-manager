from flask import Blueprint, render_template, request, redirect, url_for
from typing import List
import json

from data.database import db
from data.models.beer_stock import BeerStock

page = Blueprint("admin", __name__, template_folder = "templates", static_folder = "static")

@page.route("/admin", methods = ["GET", "POST"])
def admin_panel():

    # Get the stocks from the database
    beers: List[BeerStock] = db.session.execute(db.select(BeerStock)).scalars()

    # with open("data/stocks.json", encoding='utf-8') as f:
    #     stocks = json.loads(f.read())
    # beers, ingredients = stocks["beers"], stocks["ingredients"]

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

    # with open("data/ingredients.json", encoding='utf-8') as f:
    #     ingredients_list = json.loads(f.read())
    # return render_template("admin.html", beers = beers, ingredients = ingredients, ingredients_list = sorted(ingredients_list))
    return render_template("admin.html", beers = beers)

@page.route("/add-beer", methods = ["POST"])
def add_beer():
    # Get data form the form
    beer_name: str = request.form.get("beerName") or None
    beer_type: str = request.form.get("beerType") or None
    beer_degree: float = request.form.get("beerDegree") or -1

    if beer_name and beer_type and beer_degree >= 0:
        # Add the beer to the database
        beer_stock: BeerStock = BeerStock(name = beer_name, type = beer_type, degree = beer_degree)
        try:
            db.session.add(beer_stock)
            db.session.commit()
        except: 
            print(f"An error occured while trying to add the beer {beer_stock} to the database.")
    
    return redirect(url_for("admin.admin_panel"))

@page.route("/remove-beer/<int:beer_id>", methods = ["GET"])
def remove_beer(beer_id: int):
    # Get the beer from the id
    _query = db.select(BeerStock).where(BeerStock.id == beer_id)
    beer_stock: BeerStock = db.session.execute(_query).scalar_one_or_none()

    # Remove the beer from the database
    if beer_stock:
        try:
            db.session.remove(beer_stock)
            db.session.commit()
        except:
            print(f"An error occured while trying to remove the beer {beer_stock} from the database.")

    return redirect(url_for("admin.admin_panel"))