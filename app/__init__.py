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

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Register blueprints
    from .routes import (auth, plots, batches, care, harvest,
                         financial, pest, tasks, stubs)
    app.register_blueprint(auth.auth_bp, url_prefix='/api/auth')
    app.register_blueprint(plots.plots_bp, url_prefix='/api/plots')
    app.register_blueprint(batches.batches_bp, url_prefix='/api/batches')
    app.register_blueprint(care.care_bp, url_prefix='/api/care')
    app.register_blueprint(harvest.harvest_bp, url_prefix='/api/harvest')
    app.register_blueprint(financial.financial_bp, url_prefix='/api/financial')
    app.register_blueprint(pest.pest_bp, url_prefix='/api/pest')
    app.register_blueprint(tasks.tasks_bp, url_prefix='/api/tasks')

    # Stubs (still active for: sensors, weather, tank, actuators, alerts, dashboard)
    app.register_blueprint(stubs.stubs_bp, url_prefix='/api')

    return app