from flask import render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from recipes import app, db
from recipes.models import Users, Recipes, Ingredients, Category, Comments, RecipeIngredients, RecipeCategories


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recipes")
def recipes():
    return render_template("recipes.html")


@app.route("/sign_up", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Getting all data from the form
        email = request.form.get("email")
        password = request.form.get("password")
        firstname = request.form.get("firstname")

        # Validate form
        if not firstname or not email or not password:
            flash("Please fill out all required fields.")
            return redirect(url_for('signup'))

        email = email.lower()

        #check if user already exists in recipes database
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash("Email Address already exists")
            return redirect(url_for("signin"))

        # New users
        hashed_password = generate_password_hash(password)
        new_user = Users(
            firstname=firstname,
            email=email,
            password=generate_password_hash(password)
        )

        ## Putting new user in recipes database
        db.session.add(new_user)
        db.session.commit()

        # Adding new user to session cookie
        session["email"] = email
        flash("Registrattion Successful")
        return redirect(url_for('your_recipes.html')) # Take user to their recipes page

    return render_template("sign_up.html")


@app.route("/sign_in", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = requesr.form.get("password")

        if not email or not password:
            flash("Please enter both email and password.")
            return redirect(url_for(signin))

        email = email.lower()

        user = Users.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, passowrd):
            session["email"] = user.email
            flash("Login Successful")
            return redirect(url_for('your_recipes.html'))
        else:
            flash("Invalid email or password")
            return redirect(url_for('signup'))

    return render_template("sign_in.html")


@app.route("/add_recipe")
def create_recipe():
    return render_template("add_recipe.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")