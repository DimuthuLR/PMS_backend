from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from .routes import (auth, plots, batches, care, harvest,
                         financial, pest, tasks,
                         actuators, tank, sensors, weather,
                         alerts, dashboard, users)

    app.register_blueprint(auth.auth_bp, url_prefix='/api/auth')
    app.register_blueprint(plots.plots_bp, url_prefix='/api/plots')
    app.register_blueprint(batches.batches_bp, url_prefix='/api/batches')
    app.register_blueprint(care.care_bp, url_prefix='/api/care')
    app.register_blueprint(harvest.harvest_bp, url_prefix='/api/harvest')
    app.register_blueprint(financial.financial_bp, url_prefix='/api/financial')
    app.register_blueprint(pest.pest_bp, url_prefix='/api/pest')
    app.register_blueprint(tasks.tasks_bp, url_prefix='/api/tasks')
    app.register_blueprint(actuators.actuators_bp, url_prefix='/api/actuators')
    app.register_blueprint(tank.tank_bp, url_prefix='/api/tank')
    app.register_blueprint(sensors.sensors_bp, url_prefix='/api/sensors')
    app.register_blueprint(weather.weather_bp, url_prefix='/api/weather')
    app.register_blueprint(alerts.alerts_bp, url_prefix='/api/alerts')
    app.register_blueprint(dashboard.dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(users.users_bp, url_prefix='/api/users')

    return app