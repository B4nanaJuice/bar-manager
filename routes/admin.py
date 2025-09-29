from flask import Blueprint, render_template, request, redirect, url_for
from typing import List
import json

from data.database import db
from data.models.beer_stock import BeerStock
from data.models.ingredient_stock import IngredientStock
from data.models.cocktail_ingredient import CocktailIngredient

page = Blueprint("admin", __name__, template_folder = "templates", static_folder = "static", url_prefix = "/admin")

@page.before_request
def check_admin():
    pass

@page.route("/", methods = ["GET", "POST"])
def admin_panel():
    # Get the stocks from the database
    beers: List[BeerStock] = db.session.execute(db.select(BeerStock)).scalars()
    ingredient_stock: List[str] = list(db.session.execute(db.select(IngredientStock.name)).scalars())
    ingredients: List[str] = list(set(db.session.execute(db.select(CocktailIngredient.name)).scalars()))

    print([_ for _ in ingredient_stock])
    print(ingredients)

    return render_template("admin.html", beers = beers, ingredient_stock = ingredient_stock, ingredients = ingredients, page_title = "Panel admin")

@page.route("/add-beer", methods = ["POST"])
def add_beer():
    # Get data form the form
    beer_name: str = request.form.get("beerName") or None
    beer_type: str = request.form.get("beerType") or None
    beer_degree: float = int(request.form.get("beerDegree") or -1)

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
            db.session.delete(beer_stock)
            db.session.commit()
        except:
            print(f"An error occured while trying to remove the beer {beer_stock} from the database.")

    return redirect(url_for("admin.admin_panel"))

@page.route("/update-ingredients-stocks", methods = ["POST"])
def update_ingredients_stock():
    # Get all the ingredients and remove them
    _query = db.select(IngredientStock)
    ingredients_stock: List[IngredientStock] = db.session.execute(_query).scalars()
    try:
        for _ in ingredients_stock:
            db.session.delete(_)
        db.session.commit()
    except:
        print(f"An error occured while trying to delete an ingredient.")

    # Get the new ingredients
    new_stock: List[str] = [i for i in request.form if request.form.get(i) == 'on']

    ingredients_stock = [IngredientStock(name = _) for _ in new_stock]
    try:
        db.session.add_all(ingredients_stock)
        db.session.commit()
    except:
        print("An error occured while trying to add ingredients to the stock.")

    # Redirect to admin panel
    return redirect(url_for('admin.admin_panel'))