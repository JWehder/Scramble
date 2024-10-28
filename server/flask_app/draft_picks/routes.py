from flask import jsonify, abort
from . import draft_picks_bp  # Import the blueprint from __init__.py
import sys
import os
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db
from . import DraftPick

draft_picks_collection = db.draftPicks

@draft_picks_bp.route('/draft_picks/drafts/<draft_id>', methods=['GET'])
def get_draft_picks(draft_id):
    """Lists all draft picks by draft ID"""
    draft_picks_data = list(draft_picks_collection.find_one({"_id": ObjectId(draft_id)}))
    if draft_picks_data:
        draft_picks = []
        for draft_pick in draft_picks_data:
            draft_pick = DraftPick(**draft_picks_data)
            draft_picks.append(draft_pick)
        return jsonify({
            draft_picks
        })
    return abort(404, description="No draft picks were found for this draft.")

@draft_picks_bp.route('/draft_picks/teams/<team_id>', methods=['GET'])
def get_draft_picks_by_team_id(team_id):
    """Fetches draft pick by its team ID"""
    draft_picks_data = list(draft_picks_collection.find_one({"_id": ObjectId(team_id)}))
    if draft_picks_data:
        draft_picks = []
        for draft_pick in draft_picks_data:
            draft_pick = DraftPick(**draft_picks_data)
            draft_picks.append(draft_pick)
        return jsonify({
            draft_picks
        })
    return abort(404, description="No draft picks were found for this draft.")