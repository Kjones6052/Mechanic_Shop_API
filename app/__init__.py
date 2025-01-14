# This file is responsible for creating the application instance

# Imports
from flask import Flask
from app.models import db
from app.extensions import ma
from app.blueprints.customers import customers_bp
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.service_tickets import service_tickets_bp

# Create App Instance
def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    # Add extensions to app
    db.init_app(app) 
    ma.init_app(app)

    # Registering blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service_tickets')

    return app