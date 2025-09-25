import json 

if __name__ == '__main__':
    # Get cocktails from the cocktails.json file
    with open('data/cocktails.json', mode = 'r', encoding = 'utf-8') as f:
        cocktails = json.loads(f.read())

    # Get every ingredients from the cocktails
    ingredients = []
    for cocktail in cocktails:
        ingredients += [_['name'] for _ in cocktail['ingredients']]

    ingredients = list(set(ingredients))

    # Write the new data
    with open('data/ingredients.json', mode = 'w', encoding = 'utf-8') as f:
        f.write(json.dumps(ingredients))