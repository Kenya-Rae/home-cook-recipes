from flask import render_template
from recipes import app, db


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recipes")
def recipes():
    return render_template("recipes.html")


@app.route("/create")
def create():
    return render_template("create-recipe.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")