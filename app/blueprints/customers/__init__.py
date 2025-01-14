# This file is for linking blueprints and routes related to Customers

# Import Blueprint and instantiate
from flask import Blueprint
customers_bp = Blueprint('customers_bp', __name__)

# Import routes
from . import routes