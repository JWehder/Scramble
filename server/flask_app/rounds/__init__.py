from flask import Blueprint

rounds_bp = Blueprint('rounds', __name__)

from . import routes  # Import routes to register with the blueprint