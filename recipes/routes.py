from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from recipes import app, db
from recipes.models import Users, Recipes, Instructions, Ingredients, Category, Comments, RecipeIngredients, RecipeCategories
from werkzeug.utils import secure_filename
import time
import os


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recipes")
def recipes():
    all_recipes = Recipes.query.all()

    return render_template("recipes.html", recipes=all_recipes)


@app.route("/sign_up", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Getting all data from the form
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")

        # Validate form
        if not username or not email or not password:
            flash("Please fill out all required fields.", "error")
            return redirect(url_for('signup'))

        email = email.lower()

        #check if user already exists in recipes database
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash("Email Address already exists!", "error")
            return redirect(url_for("signin"))

        # New users
        hashed_password = generate_password_hash(password)
        new_user = Users(
            username=username,
            email=email,
            password=hashed_password
        )

        ## Putting new user in recipes session
        db.session.add(new_user)
        db.session.commit()

        # Adding new user to session cookie
        session["email"] = new_user.email
        flash("Sign Up Successful!", "success")

        return redirect(url_for('dashboard')) # Take user to their recipes page

    return render_template("sign_up.html")


@app.route("/sign_in", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Please enter both email and password.", "error")
            return redirect(url_for('signin'))

        email = email.lower()
        user = Users.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["email"] = user.email
            flash("Login Successful! Welcome!", "successful")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password", "error")
            return redirect(url_for('signup'))
    
    return render_template("sign_in.html")


@app.route("/dashboard")
def dashboard():
    if 'email' not in session:
        flash('Please sign in.', "error")
        return redirect(url_for('signin'))

    # Getting logged in user
    user = Users.query.filter_by(email=session["email"]).first()

    # check if the user exists
    if not user:
        flash('Please sign in.', "error")
        return redirect(url_for('signin'))

    user_recipes = Recipes.query.filter_by(user_id=user.id).all()

    return render_template('dashboard.html', user=user, recipes=user_recipes)
    

@app.route("/logout")
def logout():
    # removing user from session
    flash('You have been logged out.', "success")
    session.pop("email")
    return redirect(url_for("signin"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if 'email' not in session:
        flash('Please sign in to add a recipe.', "error")
        return redirect(url_for('signin'))

    user = Users.query.filter_by(email=session["email"]).first()  # Get the current user
    if request.method == "POST":
        title = request.form.get("name")
        description = request.form.get("description")
        prep_time = request.form.get("preptime")
        cook_time = request.form.get("cooktime")
        servings = request.form.get("servings")

        # Image handling
        image_file = request.files.get('recipe_image')
        image_filename = None

        # Create the images directory if it doesn't exist
        image_dir = 'static/images'
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        if image_file:
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(image_dir, image_filename)
            image_file.save(image_path)

        # Create new recipe
        new_recipe = Recipes(
            title=title,
            description=description,
            prep_time=prep_time,
            cook_time=cook_time,
            total_time=int(prep_time) + int(cook_time),
            servings=servings,
            image_url=image_filename,
            user_id=user.id
        )
        
        db.session.add(new_recipe)
        db.session.commit()  # Commit the new recipe to get its ID

        # Handle ingredients
        ingredient_names = request.form.getlist("ingredient_name[]")
        ingredient_quantities = request.form.getlist("ingredient_quantity[]")

        for name, quantity in zip(ingredient_names, ingredient_quantities):
            ingredient = Ingredients.query.filter_by(name=name).first()
            if ingredient:
                recipe_ingredient = RecipeIngredients(
                    recipe_id=new_recipe.id,
                    ingredient_id=ingredient.id,
                    quantity=quantity
                )
                db.session.add(recipe_ingredient)
            else:
                flash(f"Ingredient {name} not found in the database.", "error")

        # Handle instructions
        instructions = request.form.getlist("instruction[]")
        for step in instructions:
            instruction = Instructions(content=step, recipe_id=new_recipe.id)
            db.session.add(instruction)

        # Handle categories
        category_ids = request.form.getlist('category_id')
        for category_id in category_ids:
            new_category = RecipeCategories(recipe_id=new_recipe.id, category_id=category_id)
            db.session.add(new_category)

        db.session.commit()  # Commit all changes
        flash('Recipe Added!', "success")
        return redirect(url_for("dashboard"))

    # Fetch all categories for the dropdown
    all_categories = Category.query.all()
    return render_template("add_recipe.html", categories=all_categories)


@app.route("/recipe/<int:recipe_id>")
def view_recipe(recipe_id):
    # Get the recipe by ID
    recipe = Recipes.query.get_or_404(recipe_id)

    # Query category
    category = recipe.categories

    return render_template("view_recipe.html", recipe=recipe, category=category)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if 'email' not in session:
        flash('Please sign in.', "error")
        return redirect(url_for('signin'))

    user = Users.query.filter_by(email=session["email"]).first()

    if not user.is_admin:
        flash("You do not have the permissions to do this.", "error")
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        category_name = request.form.get("category_name")
        
        # Check if category already exists
        existing_category = Category.query.filter_by(name=category_name).first()
        if existing_category:
            flash("Category already exists.")
            return redirect(url_for('add_category'))

        # Add new category to the db
        new_category = Category(name=category_name)
        db.session.add(new_category)
        db.session.commit()

        flash(f'Category "{category_name}" added successfully!', "sucess")
        return redirect(url_for('dashboard'))  # Go back to Dashboard

    return render_template("add_category.html")


@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = Recipes.query.get_or_404(recipe_id)

    if request.method == "POST":        
        # Handle categories
        category_ids = request.form.getlist('category_id')
        recipe.categories.clear()  # Clear current categories
        for category_id in category_ids:
            new_category = RecipeCategories(recipe_id=recipe.id, category_id=category_id)
            db.session.add(new_category)
        
        db.session.commit()
        flash('Recipe Updated!', "success")
        return redirect(url_for("dashboard"))

    # Fetch all categories for the dropdown
    all_categories = Category.query.all()
    return render_template("edit_recipe.html", recipe=recipe, categories=all_categories)


@app.route("/delete_recipe/<int:recipe_id>")
def delete_recipe(recipe_id):
    recipe = Recipes.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for("dashboard"))


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


@app.route("/make_me_admin")
def make_me_admin():
    # Check if the user is logged in
    if 'email' not in session:
        flash('Please sign in.', "error")
        return redirect(url_for('signin'))

    # Fetch the logged-in user
    current_user = Users.query.filter_by(email=session["email"]).first()

    # Make me an admin initially
    owner_email = 'kenyarae99@gmail.com'

    if current_user:
        # Ensure that only the site owner (me) can promote to admin
        if current_user.email == owner_email:
            if not current_user.is_admin:
                current_user.is_admin = True
                db.session.commit()
                flash(f'{current_user.email} has been made an admin.', "success")
            else:
                flash(f'{current_user.email} is already an admin.', "info")
        else:
            flash(f'Only the site owner can make themselves an admin.', "error")
    else:
        flash('User not found.', "error")

    return redirect(url_for('dashboard'))


@app.route("/promote_user/<int:user_id>")
def promote_user(user_id):
    # Check user is logged in
    if 'email' not in session:
        flash('Please sign in.', "error")
        return redirect(url_for('signin'))

    # Get the logged in user
    current_user = Users.query.filter_by(email=session["email"]).first()

    if current_user and current_user.is_admin:
        # Fetch the user to be promoted by ID
        user_to_promote = Users.query.get_or_404(user_id)

        # Prevent promoting the same user again
        if user_to_promote.is_admin:
            flash(f'{user_to_promote.email} is already an admin.', "info")
        else:
            user_to_promote.is_admin = True
            db.session.commit()
            flash(f'{user_to_promote.email} has been promoted to admin.', "success")
    else:
        flash('You do not have the permissions to do this.', "error")

    return redirect(url_for('dashboard'))