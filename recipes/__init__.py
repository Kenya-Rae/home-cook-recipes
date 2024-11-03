import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import current_app
from flask_mail import Mail, Message  # Import Flask-Mail

if os.path.exists("env.py"):
    import env  # noqa

# Initialize Flask app
app = Flask(__name__)

# Function for current_app
def currentApp_function():
    with current_app.app_context():
        print(current_app.config['SECRET_KEY'])

# Configurations
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Replace with your SMTP server
app.config['MAIL_PORT'] = 587 
app.config['MAIL_USE_TLS'] = True  # Use TLS (True or False)
app.config['MAIL_USE_SSL'] = False  # Use SSL (True or False)
app.config['MAIL_USERNAME'] = 'your_email@example.com'  # Your email
app.config['MAIL_PASSWORD'] = 'your_email_password'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'  # Default sender

# Image upload settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipes/static/images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size (16MB)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)  # Initialize Flask-Mail with the app

from recipes import routes # noqa