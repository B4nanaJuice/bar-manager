from flask import Blueprint, request, json

from data.database import db
from data.models.order import Order

page = Blueprint("api", __name__, url_prefix = "/api")

@page.route("/order-cocktail", methods = ['GET'])
def order_cocktail() -> dict:
    try:
        cocktail_id: int = request.args.get("cocktail-id", type = int)
        client_name: str = request.args.get("client-name", type = str)
    except:
        print("Error")
        return "Error in url arguments.", 400
    
    if not cocktail_id or not client_name:
        return "Error in url arguments.", 400
    
    order: Order = Order(cocktail = cocktail_id, client = client_name)

    db.session.add(order)
    db.session.commit()

    return "Successfully placed order.", 200

@page.route("/order-beer", methods = ['GET'])
def order_beer() -> dict:
    try:
        beer_id: int = request.args.get("beer-id", type = int)
        client_name: str = request.args.get("client-name", type = str)
    except:
        print("Error")
        return "Error in url arguments.", 400
    
    if not beer_id or not client_name:
        return "Error in url arguments.", 400
    
    order: Order = Order(beer = beer_id, client = client_name)

    db.session.add(order)
    db.session.commit()

    return "Successfully placed order.", 200