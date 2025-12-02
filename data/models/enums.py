from enum import Enum

class CocktailType(Enum):
    SHOT = 'shot'
    SHORT = 'short'
    LONG = 'long'

class Glass(Enum):
    SHOT = 'shot'
    MARTINI = 'martini'
    OLD_FASHIONED = 'old_fashioned'
    TUMBLER = 'tumbler'
    TIKI = 'tiki'

class MixMethod(Enum):
    DIRECT = 'direct'
    SHAKER = 'shaker'
    MIXING_GLASS = 'mixing_glass'

class BeerType(Enum):
    BLANCHE = 'blanche'
    BLONDE = 'blonde'
    AMBREE = 'ambrée'
    BRUNE = 'brune'

class TagName(Enum):
    # Profil gustatif
    SUCRE = 'sucré'
    ACIDE = 'acide'
    AMER = 'amer'
    SALE = 'salé'
    UMAMI = 'umami'
    EPICE = 'épicé'
    FRUITE = 'fruité'
    FLORAL = 'floral'
    HERBACE = 'herbacé'
    FUME = 'fumé'
    BOISE = 'boisé'
    CREMEUX = 'crémeux'

    # Texture / sensation en bouche
    SEC = 'sec'
    DOUX = 'doux'
    ONCTUEUX = 'onctueux'
    VELOUTE = 'velouté'
    PETILLANT = 'pétillant'
    SIRUPEUX = 'sirupeux'
    AERIEN = 'aérien'

    # Occasion
    RAFRAICHISSANT = 'rafraîchissant'
    DIGESTIF = 'digestif'
    APERITIF = 'apéritif'
    CONFORT = 'confort'
    ESTIVAL = 'estival'
    HIVERNAL = 'hivernal'

    # Spiritueux de base
    GIN = 'gin-based'
    VODKA = 'vodka-based'
    RHUM = 'rhum-based'
    WHISKY = 'whisky-based'
    TEQUILA = 'tequila-based'
    MEZCAL = 'mezcal-based'
    BRANDY = 'brandy-based'
    WINE = 'wine-based'
