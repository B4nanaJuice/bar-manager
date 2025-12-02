from flask import Blueprint, request, render_template

from data.database import db
from data.models.cocktail import Cocktail
from data.models.beer import Beer
from data.models.drink import Drink
from data.models.tag import Tag
from data.models.enums import CocktailType, BeerType, TagName

from sqlalchemy.sql.functions import func

page = Blueprint(name = 'public', import_name = __name__, url_prefix = '', template_folder = 'templates', static_folder = 'static')

@page.route('/', methods = ['GET'])
@page.route('/home', methods = ['GET'])
def home():
    return render_template('public/home.html')

@page.route('/cocktails', methods = ['GET', 'POST'])
def cocktails():

    # Base query
    _query = db.select(Cocktail).where(Cocktail.is_available)

    search: dict = {}

    if request.method == 'POST':

        # Get data from form
        ## Get cocktail name
        cocktail_name: str | None = request.form.get('cocktail-name') or None

        ## Get cocktail type
        cocktail_type: str = request.form.get('cocktail-type').upper() or None
        if cocktail_type and cocktail_type in CocktailType.__members__:
            cocktail_type: CocktailType = CocktailType[cocktail_type]
        else:
            cocktail_type = None

        ## Get if the user wants mocktails
        no_alcohol: bool = request.form.get('no-alcohol') != None

        ## Get the tag
        tag: str | None = request.form.get('tag') or None
        if tag == 'all':
            tag = None
        if tag and tag in TagName.__members__:
            tag: TagName = TagName[tag]
        else:
            tag = None

        # Add queries if filters
        ## Filter by name
        if cocktail_name:
            _query = _query.where(Cocktail.name.ilike(f'%{cocktail_name}%'))

        ## Filter by type
        if cocktail_type:
            _query = _query.where(Cocktail.type == cocktail_type)

        ## Filter by alcohol presence
        if no_alcohol:
            _query = _query.where(Cocktail.has_alcohol == False)

        ## Filter by tag
        if tag:
            _query = _query.where(Drink.tags.any(Tag.name == tag))

        # Generate search values (prefill the search bar)
        search = {
            'cocktail_name': cocktail_name,
            'cocktail_type': cocktail_type,
            'no_alcohol': no_alcohol,
            'tag': tag
        }

    cocktails: list[Cocktail] = list(db.paginate(_query))

    enums = {
        'cocktailType': CocktailType,
        'tagName': TagName
    }

    return render_template('public/cocktails.html', cocktails = cocktails, enums = enums, search = search)

@page.route('/beers', methods = ['GET', 'POST'])
def beers():

    # Base query
    _query = db.select(Beer).where(Beer.is_available)

    search: dict = {}

    if request.method == 'POST':

        # Get data from form
        ## Get the beer type
        beer_type: str = request.form.get('beer-type').upper() or None
        if beer_type and BeerType.__members__:
            beer_type: BeerType = BeerType[beer_type]
        else:
            beer_type = None

        ## Get the beer degree
        beer_degree_min: float = request.form.get('beer-degree-min') or 0
        beer_degree_max: float = request.form.get('beer-degree-max') or 50

        ## Get the tag
        tag: str | None = request.form.get('tag') or None
        if tag == 'all':
            tag = None
        if tag and tag in TagName.__members__:
            tag: TagName = TagName[tag]
        else:
            tag = None

        # Add queries if filters
        ## Filter by type
        if beer_type:
            _query = _query.where(Beer.type == beer_type)

        ## Filter by beer degree
        if beer_degree_min:
            _query = _query.where(Beer.degree >= beer_degree_min)

        if beer_degree_max:
            _query = _query.where(Beer.degree <= beer_degree_max)

        ## Filter by tag
        if tag:
            _query = _query.where(Drink.tags.any(Tag.name == tag))

        # Generate search values (prefill the search bar)
        search = {
            'beer_type': beer_type,
            'beer_degree_min': beer_degree_min,
            'beer_degree_max': beer_degree_max,
            'tag': tag
        }

    beers: list[Beer] = list(db.paginate(_query))

    enums = {
        'beerType': BeerType,
        'tagName': TagName
    }

    return render_template('public/beers.html', beers = beers, enums = enums, search = search)

@page.route('/others', methods = ['GET'])
def others():
    drinks: list[Drink] = list(db.session.execute(db.select(Drink).where(Drink.is_available)).scalars())
    return "Autres-"

@page.route('/random-cocktail', methods = ['GET'])
def random_cocktail():
    cocktail: Cocktail = db.session.execute(db.select(Cocktail).order_by(func.random()).limit(1)).scalar_one()
    print(cocktail)
    return f'sqd'