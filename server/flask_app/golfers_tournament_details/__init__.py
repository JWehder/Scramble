from flask import Blueprint

golfers_tournament_details_bp = Blueprint('golfers_tournament_details', __name__)

from . import routes  # Import routes to register with the blueprint