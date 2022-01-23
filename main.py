from flask_login import current_user
from website import create_app
from flask import Blueprint, render_template
import requests
import json

app = create_app()

@app.route('/random')
def randomCocktail():
    request = requests.get('https://www.thecocktaildb.com/api/json/v1/1/random.php')
    cocktails = request.content
    images = request.content
    data = json.loads(cocktails)
    imageData = json.loads(images)

    images = []

    for image in imageData["drinks"]:
        image = {
            "image": image["strDrinkThumb"]
        }
        images.append(image)


    cocktails = []

    for cocktail in data["drinks"]:
        cocktail = {
            "Drink Name": cocktail["strDrink"],
            "Category": cocktail["strCategory"],
            "Alcohol": cocktail["strAlcoholic"],
            "Glass": cocktail["strGlass"],
            "Instructions": cocktail["strInstructions"],
            "Ingredient 1": cocktail["strIngredient1"],
            "Ingredient 2": cocktail["strIngredient2"],
            "Ingredient 3": cocktail["strIngredient3"],
            "Ingredient 4": cocktail["strIngredient4"],
            "Ingredient 5": cocktail["strIngredient5"],
            "Ingredient 6": cocktail["strIngredient6"],
            "Ingredient 7": cocktail["strIngredient7"],
            "Measurement1": cocktail["strMeasure1"],
            "Measurement2": cocktail["strMeasure2"],
            "Measurement3": cocktail["strMeasure3"],
            "Measurement4": cocktail["strMeasure4"],
            "Measurement5": cocktail["strMeasure5"],
            "Measurement6": cocktail["strMeasure6"],
            "Measurement7": cocktail["strMeasure7"]
        }

        cocktails.append(cocktail)

    return render_template('random.html', cocktail=cocktail, image=image, user=current_user)


if __name__ == "__main__":
    app.run()