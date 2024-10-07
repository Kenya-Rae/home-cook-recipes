from flask import render_template
from recipes import app, db
from recipes.models import Users, Recipes, Ingredients, Category, Comments, RecipeIngredients, RecipeCategories


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recipes")
def recipes():
    return render_template("recipes.html")


@app.route("/sign_up")
def signup():
    return render_template("sign_up.html")

@app.route("/sign_in")
def signin():
    return render_template("sign_in.html")

@app.route("/add_recipe")
def create_recipe():
    return render_template("add_recipe.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")