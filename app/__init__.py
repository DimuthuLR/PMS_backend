from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Config

# Initialize extensions (these will be used in models and routes)
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)  # Allows your frontend (running on localhost:5173) to call this backend

    # Register routes (we will add our auth routes here later)
    from .routes import auth
    app.register_blueprint(auth.auth_bp, url_prefix='/api/auth')

    return app