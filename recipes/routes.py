from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from recipes import app, db
from recipes.models import Users, Recipes, Instructions, Ingredients, Category, Comments, RecipeIngredients, RecipeCategories
from werkzeug.utils import secure_filename
from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
import time
import os


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recipes")
def recipes():
    category_id = request.args.get('category')  # Get the selected category

    if category_id:
        # Filter recipes by the selected category
        all_recipes = Recipes.query.join(RecipeCategories).filter(RecipeCategories.category_id == category_id).all()
    else:
        # Get all recipes if no category is selected
        all_recipes = Recipes.query.all()

    # Get all categories for the filter dropdown
    categories = Category.query.all()

    return render_template("recipes.html", recipes=all_recipes, categories=categories)


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

        # Check if user already exists in recipes database
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

        # Putting new user in recipes session
        db.session.add(new_user)
        db.session.commit()

        # Adding new user to session cookie
        session["email"] = new_user.email
        flash("Sign Up Successful!", "success")

        return redirect(url_for('dashboard'))  # Take user to their recipes page

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
            flash("Login Successful! Welcome!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password", "error")
            return redirect(url_for('signup'))
    
    return render_template("sign_in.html")

# Helper function to create token
def create_reset_token(user_id):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(user_id, salt="password-reset-salt")

# Helper function to verify token
def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        user_id = serializer.loads(token, salt="password-reset-salt", max_age=expiration)
    except Exception as e:
        current_app.logger.error(f'Token verification failed: {e}')
        return None
    return user_id


# If user come across a 405 error, display message and send to sign in
@app.errorhandler(405)
def method_not_allowed(error):
    flash("Method not allowed!", "error")
    return redirect('/sign_in')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        data = request.get_json() 
        email = data.get("email") 
        
        user = Users.query.filter_by(email=email).first()
        
        if user:
            token = create_reset_token(user.id)
            current_app.logger.info(f'Token created for user {user.id}: {token}')  # Log token creation
            reset_url = f"https://8080-kenyarae-homecookrecipe-3uygnjxl4z4.ws.codeinstitute-ide.net/{token}" 
            subject = "Password Reset Request"
            body = f"To reset your password, visit the following link: {reset_url}"
            send_email(email, subject, body)
            return {"status": "success"}, 200
        else:
            return {"status": "error", "message": "Email not found."}, 404
    
    return render_template('forgot_password.html')


def reset_password(token):
    user_id = verify_reset_token(token)
    if not user_id:
        flash("The reset link is invalid or has expired.", "danger")
        return redirect(url_for("signin"))
    
    # Log user ID retrieved from token for debugging
    current_app.logger.info(f'User ID from token: {user_id}')
    
    user = Users.query.get(user_id)
    if request.method == "POST":
        new_password = request.form.get("password")
        user.password = generate_password_hash(new_password)
        db.session.commit()
        flash("Your password has been reset. You can now log in.", "success")
        return redirect(url_for("signin"))

    return render_template("reset_password.html", token=token)


@app.route("/dashboard")
def dashboard():
    if 'email' not in session:
        flash('Please sign in.', "error")
        return redirect(url_for('signin'))

    # Getting logged in user
    user = Users.query.filter_by(email=session["email"]).first()

    # Check if the user exists
    if not user:
        flash('Please sign in.', "error")
        return redirect(url_for('signin'))

    user_recipes = Recipes.query.filter_by(user_id=user.id).all()

    return render_template('dashboard.html', user=user, recipes=user_recipes)
    

@app.route("/logout")
def logout():
    # Removing user from session
    flash('You have been logged out.', "success")
    session.pop("email")
    return redirect(url_for("signin"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if 'email' not in session:
        flash('Please sign in to add a recipe.', "error")
        return redirect(url_for('signin'))

    user = Users.query.filter_by(email=session["email"]).first()

    # Fetch categories from the database to pass to the template
    categories = Category.query.all()
    print(categories)

    if request.method == "POST":
        title = request.form.get("name")
        description = request.form.get("description")
        prep_time = request.form.get("preptime")
        cook_time = request.form.get("cooktime")
        servings = request.form.get("servings")

        # Handle image upload
        image_file = request.files.get('recipe_image')
        image_filename = None
        if image_file:
            image_filename = secure_filename(image_file.filename)
            upload_folder = 'recipes/static/images'
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            image_file.save(os.path.join(upload_folder, image_filename))

        # Create new recipe
        new_recipe = Recipes(
            title=title,
            description=description,
            prep_time=int(prep_time) if prep_time.isdigit() else None,
            cook_time=int(cook_time) if cook_time.isdigit() else None,
            total_time=(int(prep_time) + int(cook_time)) if prep_time.isdigit() and cook_time.isdigit() else None,
            servings=int(servings) if servings.isdigit() else None,
            image_url=image_filename or 'default.jpg',
            user_id=user.id
        )

        db.session.add(new_recipe)
        db.session.flush()  # Get new_recipe.id

        def process_ingredients(names, quantities, recipe_id):
            for name, quantity in zip(names, quantities):
                quantity = quantity.strip()  # Remove whitespace
                if not quantity:  # If quantity is empty or None, set a default value
                    print(f"Warning: Quantity for ingredient '{name}' is not valid. Defaulting to '0'.")
                    quantity = "0"  # Set a default value or decide how to handle it
                
                # Fetch or create ingredient
                ingredient = Ingredients.query.filter_by(name=name).first()
                if not ingredient:
                    ingredient = Ingredients(name=name, quantity=quantity)  # Create with quantity
                    db.session.add(ingredient)
                    db.session.flush()  # Assign ID to the new ingredient
                else:
                    # Update ingredient quantity if necessary (or ignore)
                    print(f"Using existing ingredient: {ingredient.name}")

                # Create RecipeIngredients entry
                recipe_ingredient = RecipeIngredients(
                    recipe_id=recipe_id,
                    ingredient_id=ingredient.id,
                    quantity=quantity  # Use the provided quantity
                )
                db.session.add(recipe_ingredient)

        # Process ingredients
        ingredient_names = request.form.getlist("ingredient_name[]")
        ingredient_quantities = request.form.getlist("ingredient_quantity[]")
        process_ingredients(ingredient_names, ingredient_quantities, new_recipe.id)

        # Process instructions
        instructions = request.form.getlist("instruction[]")
        for idx, step in enumerate(instructions, start=1):
            instruction = Instructions(step_number=idx, content=step, recipe_id=new_recipe.id)
            db.session.add(instruction)

        # Process categories
        category_ids = request.form.getlist('category_id[]')
        for category_id in category_ids:
            new_category = RecipeCategories(recipe_id=new_recipe.id, category_id=category_id)
            db.session.add(new_category)

        db.session.commit()
        flash("Recipe added successfully!", "success")
        return redirect(url_for("dashboard"))

    # Render the template with categories
    return render_template("add_recipe.html", categories=categories)


@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    recipe = Recipes.query.get_or_404(recipe_id)  # Get the recipe or 404 if not found
    ingredients = RecipeIngredients.query.filter_by(recipe_id=recipe.id).all() # Grabbing ingredients for the recipe
    comments = Comments.query.filter_by(recipe_id=recipe.id).order_by(Comments.created.desc()).all()  # Fetch comments for this recipe
    
    return render_template('view_recipe.html', recipe=recipe, ingredients=ingredients, comments=comments)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if 'email' not in session:
        flash('Please sign in.', "error")
        return redirect(url_for('signin'))

    user = Users.query.filter_by(email=session["email"]).first()

    if not user.is_admin:
        flash('You do not have the permissions to do this.', "error")
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

        flash(f'Category "{category_name}" added successfully!', "success")
        return redirect(url_for('dashboard'))  # Go back to Dashboard

    return render_template("add_category.html")


@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if 'email' not in session:
        flash('Please sign in to edit a recipe.', "error")
        return redirect(url_for('signin'))

    # Fetch the recipe to be edited
    recipe = Recipes.query.get(recipe_id)
    
    # Fetch categories to populate the dropdown in the template
    categories = Category.query.all()

    if request.method == "POST":
        # Updated field names to match template form
        recipe.title = request.form.get("recipe_name")
        recipe.description = request.form.get("recipe_description")
        recipe.prep_time = request.form.get("preptime")
        recipe.cook_time = request.form.get("cooktime")
        recipe.servings = request.form.get("servings")

        # Handle image upload
        image_file = request.files.get('recipe_image')
        if image_file:
            image_filename = secure_filename(image_file.filename)
            upload_folder = 'recipes/static/images'
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            image_file.save(os.path.join(upload_folder, image_filename))
            recipe.image_url = image_filename  # Update recipe with new image

        db.session.commit()
        flash("Recipe updated successfully!", "success")
        return redirect(url_for("dashboard"))

    # Pass categories to the template
    return render_template("edit_recipe.html", recipe=recipe, categories=categories)


@app.route("/delete_recipe/<int:recipe_id>", methods=["POST"])
def delete_recipe(recipe_id):
    if 'email' not in session:
        flash('Please sign in to delete a recipe.', "error")
        return redirect(url_for('signin'))

    recipe = Recipes.query.get(recipe_id)
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        flash("Recipe deleted successfully!", "success")
    else:
        flash("Recipe not found.", "error")

    return redirect(url_for("dashboard"))


@app.route("/gallery")
def gallery():
    recipes = Recipes.query.all()
    return render_template('gallery.html', recipes=recipes)


@app.route('/recipe/<int:recipe_id>/add_comment', methods=['POST'])
def add_comment(recipe_id):
    content = request.form.get('content')

    if content:
        new_comment = Comments(content=content, recipe_id=recipe_id)  # Make sure to add user_id if needed

        try:
            db.session.add(new_comment)
            db.session.commit()
            flash('Your comment has been added!', 'success')
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")  # Log the error to the console
            flash('Error adding comment. Please try again.', 'danger')
    else:
        flash('Comment cannot be empty.', 'danger')

    return redirect(url_for('view_recipe', recipe_id=recipe_id))


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


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')  # Get the search query, default to empty string if not provided
    if query:
        results = get_recipes(query)  # Call the get_recipes function to get results
    else:
        results = []  # No query means no results

    return render_template('search_results.html', results=results, query=query)  # Give back results in a template


def get_recipes(query):
    # Search for recipes based on title or ingredients
    results = Recipes.query.filter(
        (Recipes.title.ilike(f'%{query}%')) |  # For case sensitive 
        (Recipes.ingredients.any(Ingredients.name.ilike(f'%{query}%')))  # Checking ingredients
    ).all()

    return results


@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    recipe = Recipes.query.get(recipe_id)
    if recipe is None:
        flash("Recipe not found.", "error")
        return redirect(url_for("recipes"))
    return render_template("recipe_detail.html", recipe=recipe)