# This file is for linking blueprints and routes

# Import Blueprint and instantiate
from flask import Blueprint
parts_bp = Blueprint('parts_bp', __name__)

# Import routes
from . import routes