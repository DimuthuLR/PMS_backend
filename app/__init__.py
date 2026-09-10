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
    CORS(app)  # Allows your frontend to call this backend

    # ✅ Register blueprints
    from .routes import auth, plots, batches, stubs
    app.register_blueprint(auth.auth_bp, url_prefix='/api/auth')
    app.register_blueprint(plots.plots_bp, url_prefix='/api/plots')
    app.register_blueprint(batches.batches_bp, url_prefix='/api/batches')

    # ✅ Stub endpoints (to be replaced module-by-module)
    app.register_blueprint(stubs.stubs_bp, url_prefix='/api')

    return app