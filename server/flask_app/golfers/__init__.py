from flask import Blueprint

golfers_bp = Blueprint('golfers', __name__)

from . import routes  # Import routes to register with the blueprint
