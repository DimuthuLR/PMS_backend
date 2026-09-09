from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    from .routes.auth import auth_bp
    from .routes.plots import plots_bp
    from .routes.batches import batches_bp
    from .routes.care import care_bp
    from .routes.harvest import harvest_bp
    from .routes.financial import financial_bp
    from .routes.pest import pest_bp
    from .routes.tasks import tasks_bp
    from .routes.actuators import actuators_bp
    from .routes.tank import tank_bp
    from .routes.sensors import sensors_bp
    from .routes.weather import weather_bp
    from .routes.alerts import alerts_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(plots_bp, url_prefix='/api/plots')
    app.register_blueprint(batches_bp, url_prefix='/api/batches')
    app.register_blueprint(care_bp, url_prefix='/api/care')
    app.register_blueprint(harvest_bp, url_prefix='/api/harvest')
    app.register_blueprint(financial_bp, url_prefix='/api/financial')
    app.register_blueprint(pest_bp, url_prefix='/api/pest')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    app.register_blueprint(actuators_bp, url_prefix='/api/actuators')
    app.register_blueprint(tank_bp, url_prefix='/api/tank')
    app.register_blueprint(sensors_bp, url_prefix='/api/sensors')
    app.register_blueprint(weather_bp, url_prefix='/api/weather')
    app.register_blueprint(alerts_bp, url_prefix='/api/alerts')

    from .models import (
        User, Plot, Batch, CareLog, Harvest, Financial, Pest, Task,
        Actuator, Tank, Sensor, Weather, Alert
    )

    return app