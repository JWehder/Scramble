from flask import Blueprint

tournaments_bp = Blueprint('tournaments', __name__)

from . import routes  # Import routes to register with the blueprint