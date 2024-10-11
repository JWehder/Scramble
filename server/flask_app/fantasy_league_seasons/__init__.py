from flask import Blueprint

leagues_settings_bp = Blueprint('leagues_settings', __name__)

from . import routes  # Import routes to register with the blueprint