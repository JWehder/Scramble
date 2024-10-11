from flask import Blueprint

holes_bp = Blueprint('holes', __name__)

from . import routes  # Import routes to register with the blueprint