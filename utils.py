import json

def get_available_cocktails(available_ingredients: list) -> list:
    with open("data/cocktails.json", encoding='utf-8') as f:
        cocktails: list = json.loads(f.read())

    available_cocktails: list = []
    for cocktail in cocktails:
        cocktail_ingredients = [ingredient["name"] for ingredient in cocktail["ingredients"]]
        if len(list(set(cocktail_ingredients) - set(available_ingredients))) == 0:
            available_cocktails.append(cocktail)

    return available_cocktails