# This file is for linking blueprints and routes related to Service Tickets

# Import Blueprint and instantiate
from flask import Blueprint
service_tickets_bp = Blueprint('service_tickets_bp', __name__)

# Import routes
from . import routes