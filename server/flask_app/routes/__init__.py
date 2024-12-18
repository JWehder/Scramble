# routes/__init__.py
from .leagues import leagues_bp
from .periods import periods_bp
from .teams import teams_bp
from .fantasy_league_seasons import fantasy_league_seasons_bp
from .draft_picks import draft_picks_bp
from .drafts import drafts_bp
from .golfers import golfers_bp
from .golfer_tournament_details import golfer_tournament_details_bp
from .holes import holes_bp
from .rounds import rounds_bp
from .team_results import team_results_bp
from .users import users_bp
from .league_settings import league_settings_bp
from .tournaments import tournaments_bp

# Make blueprints accessible for importing
__all__ = [
    'leagues_bp', 'periods_bp', 'teams_bp', 'fantasy_league_seasons_bp',
    'draft_picks_bp', 'drafts_bp', 'golfers_bp', 'golfer_tournament_details_bp',
    'holes_bp', 'rounds_bp', 'team_results_bp', 'users_bp',
    'league_settings_bp', 'tournaments_bp'
]
