from flask import Blueprint, request, jsonify

from data.database import db
from data.models.order import Order
from data.models.cocktail import Cocktail
from data.models.beer_stock import BeerStock

page = Blueprint("api", __name__, url_prefix = "/api")

@page.route("/order-cocktail", methods = ['GET'])
def order_cocktail() -> dict:
    try:
        cocktail_id: int = request.args.get("cocktail-id", type = int)
        client_name: str = request.args.get("client-name", type = str)
    except:
        return jsonify({
            "response": "Error in url parameters",
            "status": 400
        })
    
    if not cocktail_id or not client_name or cocktail_id == "" or client_name == "":
        return jsonify({
            "response": "Missing url parameters",
            "status": 400
        })
    
    cocktail: Cocktail = db.session.execute(db.select(Cocktail).where(Cocktail.id == cocktail_id)).scalar_one_or_none()
    if not cocktail:
        return jsonify({
            "response": "Unable to find cocktail",
            "status": 400
        })
    
    try:
        order: Order = Order(cocktail = cocktail, client = client_name)

        db.session.add(order)
        db.session.commit()
    except:
        return jsonify({
            "response": "Error while trying to insert order into database",
            "status": 400
        })

    return jsonify({
            "response": "Successfully placed order",
            "status": 200
        })


@page.route("/order-beer", methods = ['GET'])
def order_beer() -> dict:
    try:
        beer_id: int = request.args.get("beer-id", type = int)
        client_name: str = request.args.get("client-name", type = str)
    except:
        return jsonify({
            "response": "Error in url parameters",
            "status": 400
        })
    
    if not beer_id or not client_name or beer_id == "" or client_name == "":
        return jsonify({
            "response": "Missing url parameters",
            "status": 400
        })
    

    beer: BeerStock = db.session.execute(db.select(BeerStock).where(BeerStock.id == beer_id)).scalar_one_or_none()
    if not beer:
        return jsonify({
            "response": "Unable to find beer",
            "status": 400
        })
        
    try:
        order: Order = Order(beer = beer, client = client_name)

        db.session.add(order)
        db.session.commit()
    except:
        return jsonify({
            "response": "Error while trying to insert order into database",
            "status": 400
        })

    return jsonify({
            "response": "Successfully placed order",
            "status": 200
        })