from recipes import db


# Link Tables

# recipe_ingredients = (

# )


# recipe_categories = (

# )


# favourites = (

# )

# Models 

class Users(db.Model):
    # schema for Users Model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(130), nullable=False)
    created = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        # __repr__ to represent itself
        return self.username, self.created, self.updated_at


class Recipes(db.Model):
    # schema for Recipes Model
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    prep_time = db.Column(db.Integer, nullable=True)
    cook_time = db.Column(db.Integer, nullable=True)
    total_time = db.Column(db.Integer, nullable=True)
    servings = db.Column(db.Integer, nullable=True)
    image_url = db.Column(db.String(400), nullable=True)
    created = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # relationship to user table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself
        return self.title, self.description, self.instructions, self.prep_time, self.cook_time, self.total_time, self.serving, self.image_url, self.created, self.updated_at


class Ingredients(db.Model):
    # schema for Ingredients Model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


class Category(db.Model):
    # schema for Categories Model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


class Comments(db.Model):
    # schema for Comments Model
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)