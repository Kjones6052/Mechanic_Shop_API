# This file is for linking blueprints and routes related to Mechanics

# Import Blueprint and instantiate
from flask import Blueprint
mechanics_bp = Blueprint('mechanics_bp', __name__)

# Import routes
from . import routes