from flask import Blueprint, request, render_template, redirect, url_for, current_app, session
import os

from data.database import db
from data.models.enums import CocktailType, Glass, MixMethod, BeerType, TagName
from data.models.cocktail import Cocktail
from data.models.cocktail_ingredient import CocktailIngredient
from data.models.beer import Beer
from data.models.drink import Drink
from data.models.order import Order
from data.models.tag import Tag

page = Blueprint(name = 'admin', import_name = __name__, url_prefix = '/admin', template_folder = 'templates', static_folder = 'static')

@page.before_request
def before_request():

    if 'auth' not in session:
        session['redirect'] = request.url_rule.rule
        current_app.logger.info(f'Someone not logged trying to access {request.url_rule.rule}. Redirecting.')
        return redirect(url_for('auth.login'))
    
    if session['auth'] != os.getenv('ADMIN_USERNAME'):
        session.pop('auth')
        session['redirect'] = request.url_rule.rule
        current_app.logger.info(f'Someone not logged trying to access {request.url_rule.rule}. Redirecting.')
        return redirect(url_for('auth.login'))
    
    pass

@page.route('/', methods = ['GET'])
def admin_panel():
    # Dashboard with cocktail count, beer count, order count, ...
    # links to go to each manage page (cocktails, beers, others, orders, ...)
    return "Panel admin"

@page.route('/manage-cocktails', methods = ['GET'])
def manage_cocktails():

    cocktails: list[Cocktail] = list(db.session.execute(db.select(Cocktail)).scalars())

    enums = {
        'cocktailType': CocktailType,
        'glass': Glass,
        'mixMethod': MixMethod,
        'tagName': TagName
    }
    
    return render_template('admin/cocktail_form.html', cocktails = cocktails, enums = enums)

@page.route('/add-cocktail', methods = ['POST'])
def add_cocktail():

    # Get data from the form 
    ## Get cocktail name
    cocktail_name: str = request.form.get('cocktail-name')

    ## Get the cocktail type
    cocktail_type: str = request.form.get('cocktail-type').upper()
    if cocktail_type not in CocktailType.__members__:
        current_app.logger.warning(f'The cocktail type {cocktail_type} is invalid.')
        return redirect(url_for('admin.manage_cocktails'))
    cocktail_type: CocktailType = CocktailType[cocktail_type]

    ## Get if the cocktail contains alcohol or not
    has_alcohol: bool = request.form.get('has-alcohol') != None

    ## Get the glass type
    glass: str = request.form.get('glass').upper()
    if glass not in Glass.__members__:
        current_app.logger.warning(f'The glass {glass} is invalid.')
        return redirect(url_for('admin.manage_cocktails'))
    glass: Glass = Glass[glass]

    ## Get the mix method
    mix_method: str = request.form.get('mix-method').upper()
    if mix_method not in MixMethod.__members__:
        current_app.logger.warning(f'The mix method {mix_method} is invalid.')
        return redirect(url_for('admin.manage_cocktails'))
    mix_method: MixMethod = MixMethod[mix_method]

    ## Get the garnish
    garnish: str | None = request.form.get('garnish') if request.form.get('garnish') != "" else None

    ## Get all the ingredients
    ingredient_names: list[str] = request.form.getlist('ingredient-name')
    ingredient_quantities: list[float] = request.form.getlist('ingredient-quantity')
    if len(ingredient_names) != len(ingredient_quantities):
        current_app.logger.warning(f'You must provide as much ingredient names ({len(ingredient_names)}) as quantities ({len(ingredient_quantities)}).')
        return redirect(url_for('admin.manage_cocktails'))
    ingredients: list[tuple[str, float]] = [(ingredient_names[_], ingredient_quantities[_]) for _ in range(len(ingredient_names))]
    ingredients: list[CocktailIngredient] = [CocktailIngredient(name = _[0], quantity = _[1]) for _ in ingredients]

    ## Get the cocktail's tags
    checkbox = [_ for _ in request.form if request.form.get(_) == 'on' and _ != 'has-alcohol']
    tags: list[Tag] = []
    for _ in checkbox:
        if _ in TagName.__members__:
            tags.append(Tag(name = TagName[_]))

    # Create the cocktial object
    cocktail: Cocktail = Cocktail(name = cocktail_name, type = cocktail_type, has_alcohol = has_alcohol, glass = glass,
                                  mix_method = mix_method, garnish = garnish, ingredients = ingredients, tags = tags)
    
    # Insert it into the database
    try:
        current_app.logger.info(f'{cocktail.name} is being inserted to the database.')
        db.session.add(cocktail)
        db.session.commit()
    except:
        current_app.logger.error('Something went wrong while trying to insert cocktail into the database.')

    return redirect(url_for('admin.manage_cocktails'))

@page.route('/remove-cocktail', methods = ['POST'])
def remove_cocktail():

    cocktail_id: int = request.form.get('cocktail-id', type = int)
    cocktail: Cocktail | None = db.session.execute(db.select(Cocktail).where(Cocktail.id == cocktail_id)).scalar_one_or_none()
    if not cocktail:
        current_app.logger.warning(f'No cocktail with id {cocktail_id} exists.')
        return redirect(url_for('admin.manage_cocktails'))
    
    try:
        current_app.logger.info(f'{cocktail.name} is being deleted.')
        db.session.delete(cocktail)
        db.session.commit()
    except:
        current_app.logger.error('Something went wrong while trying to delete the cocktail.')

    return redirect(url_for('admin.manage_cocktails'))

@page.route('/manage-beers', methods = ['GET'])
def manage_beers():

    beers: list[Beer] = list(db.session.execute(db.select(Beer)).scalars())

    enums = {
        'beerType': BeerType,
        'tagName': TagName
    }

    return render_template('admin/beer_form.html', beers = beers, enums = enums)

@page.route('/add-beer', methods = ['POST'])
def add_beer():

    # Get data from form
    ## Get the beer name
    beer_name: str = request.form.get('beer-name')

    ## Get the beer type
    beer_type: str = request.form.get('beer-type').upper()
    if beer_type not in BeerType.__members__:
        current_app.logger.warning('The beer type {beer_type} is invalid.')
        return redirect(url_for('admin.manage_beers'))
    beer_type: BeerType = BeerType[beer_type]

    ## Get the beer degree
    beer_degree: float = request.form.get('beer-degree', type = float)

    ## Get the tags for the beer
    checkbox = [_ for _ in request.form if request.form.get(_) == 'on']
    tags: list[Tag] = []
    for _ in checkbox:
        if _ in TagName.__members__:
            tags.append(Tag(name = TagName[_]))

    # Create the beer object
    beer: Beer = Beer(name = beer_name, type = beer_type, degree = beer_degree, tags = tags)

    # Append the beer to the database
    try:
        current_app.logger.info(f'{beer.name} is being inserted into the database.')
        db.session.add(beer)
        db.session.commit()
    except:
        current_app.logger.error('Something went wrong while trying to insert the beer into the database.')

    return redirect(url_for('admin.manage_beers'))

@page.route('/remove_beer', methods = ['POST'])
def remove_beer():

    beer_id: int = request.form.get('beer-id', type = int)
    beer: Beer | None = db.session.execute(db.select(Beer).where(Beer.id == beer_id)).scalar_one_or_none()
    if not beer:
        current_app.logger.warning(f'No beer with id {beer_id} exists.')
        return redirect(url_for('admin.manage_beers'))
    
    try:
        current_app.logger.info(f'{beer.name} is being deleted.')
        db.session.delete(beer)
        db.session.commit()
    except:
        current_app.logger.error('Something went wrong while trying to delete the beer.')

    return redirect(url_for('admin.manage_beers'))

@page.route('/manage-others', methods = ['GET'])
def manage_others():

    drinks: list[Drink] = list(db.session.execute(
        db.select(Drink)
        .where(Drink.drink_type != 'cocktail')
        .where(Drink.drink_type != 'beer')
    ))

    return "Manage others"

@page.route('/add_others', methods = ['POST'])
def add_others():

    drink_name: str = request.form.get('drink-name')
    
    drink_type: str = request.form.get('drink-type')

    drink: Drink = Drink(name = drink_name, drink_type = drink_type)

    try:
        current_app.logger.info(f'{drink.name} is being inserted into the database.')
        db.session.add(drink)
        db.session.commit()
    except:
        current_app.logger.error('Something went wrong while trying to insert the drink into the database.')

    return redirect(url_for('admin.manage_others'))

@page.route('/remove-others', methods = ['POST'])
def remove_others():
    
    drink_id: int = request.form.get('drink-id', type = int)
    drink: Drink | None = db.session.execute(db.select(Drink).where(Drink.id == drink_id)).scalar_one_or_none()
    if not drink:
        current_app.logger.warning(f'No beer with id {drink_id} exists.')
        return redirect(url_for('admin.manage_drinks'))
    
    try:
        current_app.logger.info(f'{drink.name} is being deleted.')
        db.session.delete(drink)
        db.session.commit()
    except:
        current_app.logger.error('Something went wrong while trying to delete the drink.')

    return redirect(url_for('admin.manage_drinks'))

@page.route('/orders', methods = ['GET'])
def orders():

    orders: list[Order] = list(db.session.execute(db.select(Order)).scalars())

    return "Commandes"

@page.route('/remove-order', methods = ['POST'])
def remove_order():

    order_id: int = request.form.get('order-id')
    order: Order | None = db.session.execute(db.select(Order).where(Order.id == order_id)).scalar_one_or_none()
    if not order:
        current_app.logger.warning(f'No order with id {order_id} exists.')
        return redirect(url_for('admin.orders'))
    
    try:
        current_app.logger.info(f'{order.name} is being deleted.')
        db.session.delete(order)
        db.session.commit()
    except:
        current_app.logger.error('Something went wrong while trying to delete the order.')

    return redirect(url_for('admin.orders'))