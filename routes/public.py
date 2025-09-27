from flask import Blueprint, redirect, url_for, render_template, request
import json
import re
from typing import List
from sqlalchemy.sql import exists

from utils import get_available_cocktails
from data.database import db
from data.models.cocktail import Cocktail
from data.models.beer_stock import BeerStock
from data.models.cocktail_ingredient import CocktailIngredient
from data.models.ingredient_stock import IngredientStock

page = Blueprint("public", __name__, template_folder = "templates", static_folder = "static")

@page.route("/", methods = ["GET"])
def home():
    return redirect(url_for("public.cocktails"))

@page.route("/populate", methods = ["GET"])
def populate():
    print([_ for _ in db.session.execute(db.select(IngredientStock)).scalars()])
    return redirect(url_for('public.cocktails'))

@page.route("/cocktails", methods = ["GET"])
def cocktails():
    # Get URL arguments
    cocktail_type: str = request.args.get("cocktail_type", default = None)
    ingredient_preferences: str = request.args.get("ingredient_preferences", default = None)
    mocktail: bool = request.args.get("no_alcohol", default = None)

    # Get available cocktails
    # available_cocktails: list[dict] = get_available_cocktails(available_ingredients)

    # if ingredient_preferences != "":
    #     ingredient_preferences: list[str] = ingredient_preferences.split(",")
    #     # Variable matches = list of tuples having : 
    #     # - in first place the cocktail itself
    #     # - in second place the number of matches between the ingredients of the cocktail and the ingredient_preferences
    #     matches: list[tuple] = [
    #             (_c, len([_ for _ in [i["name"] for i in _c["ingredients"]] if _.lower() in [i.lower() for i in ingredient_preferences]]))
    #             for _c in available_cocktails
    #         ]
    #     # Sort the mateches variable by number of matches
    #     matches = sorted(matches, key = lambda t: t[1], reverse = True)
    #     # Take only entries with at least 1 match
    #     matches = [_ for _ in matches if _[1] >= 1]

    #     available_cocktails = [_[0] for _ in matches]


    # Get the available ingredients for the cocktails
    _query = db.select(IngredientStock.name)
    available_ingredients: List[str] = db.session.execute(_query).scalars()

    # Create base query with only available ingredients
    _subquery = (
        db.select(CocktailIngredient.id)
        .where(CocktailIngredient.cocktail_id == Cocktail.id)
        .where(~CocktailIngredient.name.in_(db.session.query(IngredientStock.name)))
    )
    _query = db.select(Cocktail).where(~exists(_subquery))

    # Add additional filters depending on the URL parameter
    if cocktail_type:
        _query = _query.where(Cocktail.type == cocktail_type)

    if ingredient_preferences:
        ingredient_preferences: List[str] = ingredient_preferences.split(",")

    if mocktail:
        _query = _query.where(Cocktail.has_alcohol == False)
    
    # Query
    available_cocktails: List[Cocktail] = db.session.execute(_query).scalars()

    return render_template("cocktails.html.jinja", page_title = "Cocktails", cocktails = available_cocktails, ingredients = available_ingredients)

@page.route("/beers", methods = ["GET"])
def beers():
    # Get URL arguments
    beer_type: str = request.args.get("beer_type", default = "")

    # Get beers from type
    _query = db.select(BeerStock)
    if beer_type != "":
        _query = _query.where(BeerStock.type == beer_type)
    beers: List[BeerStock] = db.session.execute(_query).scalars()

    # Get the beer types
    _query = db.select(BeerStock.type)
    beer_types: List[str] = list(set(db.session.execute(_query).scalars()))

    # Render the template with the wanted beers
    return render_template("beers.html.jinja", page_title = "Bières", beers = beers, beer_types = beer_types)

@page.route("/others", methods = ["GET"])
def others():
    # Create base query
    _query = db.select(IngredientStock)

    # Filter to get only juices and syrups
    juices: List[IngredientStock] = db.session.execute(_query.where(IngredientStock.name.startswith("Jus"))).scalars()
    syrups: List[IngredientStock] = db.session.execute(_query.where(IngredientStock.name.startswith("Sirop"))).scalars()

    # Render the template
    return render_template("others.html.jinja", page_title = "Autres", juices = juices, syrups = syrups)