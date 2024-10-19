from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from recipes import app, db
from recipes.models import Users, Recipes, Ingredients, Category, Comments, RecipeIngredients, RecipeCategories


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
            flash("Please fill out all required fields.")
            return redirect(url_for('signup'))

        email = email.lower()

        #check if user already exists in recipes database
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash("Email Address already exists!")
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
        session["email"] = email
        flash("Sign Up Successful!")

        return redirect(url_for('dashboard')) # Take user to their recipes page

    return render_template("sign_up.html")


@app.route("/sign_in", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Please enter both email and password.")
            return redirect(url_for('signin'))

        email = email.lower()

        user = Users.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["email"] = user.email
            flash("Login Successful  Welcome, {}".format(request.form.get("username")))
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password")
            return redirect(url_for('signup'))
    
    return render_template("sign_in.html")


@app.route("/dashboard")
def dashboard():
    if 'email' not in session:
        flash('Please sign in.')
        return redirect(url_for('signin'))

    user = Users.query.filter_by(email=session["email"]).first()

    user_recipes = Recipes.query.filter_by(user_id=user.id).all()

    return render_template('dashboard.html', user=user, recipes=user_recipes)
    

@app.route("/logout")
def logout():
    # removing user from session
    flash('You have been logged out.')
    session.pop("email")
    return redirect(url_for("signin"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if 'email' not in session:
        flash('Please sign in.')
        return redirect(url_for('signin'))

    user = Users.query.filter_by(email=session["email"]).first()
    
    # Load categories from the database for both GET and POST requests
    categories = Category.query.all()

    if request.method == "POST":
        title = request.form.get("recipe_name")
        description = request.form.get("recipe_description")
        instructions = request.form.get("recipe_instructions")
        prep_time = request.form.get("preptime")
        cook_time = request.form.get("cooktime")
        servings = request.form.get("servings")
        category_ids = request.form.getlist('category_ids')
        image_url = request.files.get('recipe_image')  # handle the uploaded image

        # Code to handle saving the image
        # if image_url:
            # Save image logic here, e.g., save the file to static directory
            # image_url.save(os.path.join("static/uploads", image_url.filename))
            # pass

        # Create new recipe
        new_recipe = Recipes(
            title=title,
            description=description,
            instructions=instructions,
            prep_time=prep_time,
            cook_time=cook_time,
            total_time=int(prep_time) + int(cook_time),  # total time
            servings=servings,
            image_url=image_url.filename if image_url else None,  # Save image if one is there
            user_id=user.id  # Link recipe to the logged-in user
        )
        
        db.session.add(new_recipe)
        db.session.commit()

        # Assigning recipe to categories
        if category_ids:
            for category_id in category_ids:
                recipe_category = RecipeCategories(
                    recipe_id=new_recipe.id,
                    category_id=int(category_id)
                )
                db.session.add(recipe_category)

        db.session.commit()
        flash('Recipe added!')
        return redirect(url_for('dashboard'))

    return render_template("add_recipe.html", categories=categories)


@app.route("/recipe/<int:recipe_id>")
def view_recipe(recipe_id):
    # Get the recipe by ID
    recipe = Recipes.query.get_or_404(recipe_id)

    # Query category
    category = recipe.categories

    return render_template("view_recipe.html", recipe=recipe, category=category)


@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = Recipes.query.get_or_404(recipe_id)
    if request.method == "POST":
        title = request.form.get("recipe_name")
        description = request.form.get("recipe_description")
        instructions = request.form.get("recipe_instructions")
        prep_time = request.form.get("preptime")
        cook_time = request.form.get("cooktime")
        servings = request.form.get("servings")
        category_ids = request.form.getlist('category_ids')
        image_url = request.files.get('recipe_image')

        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template("edit_recipe.html", recipe=recipe)


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")