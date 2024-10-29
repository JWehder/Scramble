

# routes/__init__.py
from .draft_pick import draft_picks_bp
from .drafts import drafts_bp  # Example for another route module
# Import other blueprints as needed

# Make blueprints accessible for external import
__all__ = ['draft_picks_bp', 'drafts_bp']