from flask import Blueprint

drafts_bp = Blueprint('drafts', __name__)

from . import routes  # Import routes to register with the blueprint