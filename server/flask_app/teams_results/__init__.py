from flask import Blueprint

teams_bp = Blueprint('teams', __name__)

from . import routes  # Import routes to register with the blueprint