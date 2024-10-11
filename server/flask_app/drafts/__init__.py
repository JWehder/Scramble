from flask import Blueprint

drafts_picks_bp = Blueprint('draft_picks', __name__)

from . import routes  # Import routes to register with the blueprint