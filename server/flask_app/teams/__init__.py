from flask import Blueprint

pro_seasons_bp = Blueprint('pro_seasons', __name__)

from . import routes  # Import routes to register with the blueprint