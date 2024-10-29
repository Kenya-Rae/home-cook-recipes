from recipes import db
from datetime import datetime


# Models 
class Users(db.Model):
    # schema for Users Model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(260), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

    recipes = db.relationship('Recipes', back_populates='author', lazy=True)
    comments = db.relationship('Comments', back_populates='author', lazy=True)

    def __repr__(self):
        return f"<User {self.email}, (ID: {self.id})>"


class Recipes(db.Model):
    # schema for Recipes Model
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    prep_time = db.Column(db.Integer, nullable=True)
    cook_time = db.Column(db.Integer, nullable=True)
    total_time = db.Column(db.Integer, nullable=True)
    servings = db.Column(db.Integer, nullable=True)
    image_url = db.Column(db.String(400), nullable=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationship to user table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    comments = db.relationship('Comments', back_populates='recipe', lazy=True)
    ingredients = db.relationship('RecipeIngredients', back_populates='recipe', cascade='all, delete-orphan')
    categories = db.relationship('RecipeCategories', back_populates='recipe', cascade='all, delete-orphan')
    instructions = db.relationship('Instructions', back_populates='recipe', cascade='all, delete-orphan', passive_deletes=True)

    author = db.relationship('Users', back_populates="recipes")

    def __repr__(self):
        return f"<Recipe {self.title}(ID:{self.id})>"


class Instructions(db.Model):
    # schema for Instructions Model
    id = db.Column(db.Integer, primary_key=True)
    step_number = db.Column(db.Integer, nullable=False) # Ensuring order of instructions
    content = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)

    recipe = db.relationship('Recipes', back_populates='instructions')

    def __repr__(self):
        return f"<Instruction {self.content} (ID: {self.id})>"


class Ingredients(db.Model):
    # schema for Ingredients Model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    recipes = db.relationship('RecipeIngredients', back_populates='ingredient', lazy=True)

    def __repr__(self):
        return f"<Ingredient {self.name} (ID: {self.id})>"


class Category(db.Model):
    # schema for Categories Model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    recipes = db.relationship('RecipeCategories', back_populates='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.name} (ID: {self.id})>"


class Comments(db.Model):
    # schema for Comments Model
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)

    author = db.relationship('Users', back_populates='comments')
    recipe = db.relationship('Recipes', back_populates='comments')

    def __repr__(self):
        return f"Comment {self.id} on Recipe {self.recipe_id}"


class RecipeIngredients(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
    quantity = db.Column(db.String(60), nullable=False)

    recipe = db.relationship('Recipes', back_populates='ingredients')
    ingredient = db.relationship('Ingredients', back_populates='recipes')

    def __repr__(self):
        return f"<RecipeIngredient RecipeID: {self.recipe_id}, IngredientID: {self.ingredient_id}, Quantity: {self.quantity}>"


class RecipeCategories(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'), primary_key=True)

    recipe = db.relationship('Recipes', back_populates='categories')
    category = db.relationship('Category', back_populates='recipes')

    def __repr__(self):
        return f"<RecipeCategory RecipeID: {self.recipe_id}, CategoryID: {self.category_id}>"
