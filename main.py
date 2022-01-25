from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_login import current_user
from flask import Blueprint, render_template
import requests
import json

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'communism'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from website import views
    from website import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from website import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

@create_app.route('/random')
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
    create_app.run(debug=True)