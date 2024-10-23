from flask import Blueprint

fantasy_league_seasons = Blueprint('fantasy_league_seasons', __name__)

from . import routes  # Import routes to register with the blueprint