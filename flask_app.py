# This file is used to run the app

# Imports
from app import create_app
from app.models import db

# Activating DevelopmentConfig
app = create_app('DevelopmentConfig')

with app.app_context():
    db.create_all()

# Run App
app.run()