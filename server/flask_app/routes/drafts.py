from flask import jsonify, abort, Blueprint
import sys
import os
from bson.objectid import ObjectId
from ..models import Draft


# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db

drafts_collection = db.holes
drafts_bp = Blueprint('leagues_settings', __name__)


@drafts_bp.route('/drafts/<league_id>', methods=['GET'])
def get_drafts(league_id):
    """Lists all drafts by ID"""
    draft_data = list(drafts_collection.find_one({"_id": ObjectId(league_id)}))
    if draft_data:
        draft = Draft(**draft_data)
        return jsonify({
            draft
        })
    return abort(404, description="No drafts were found for this league.")

@drafts_bp.route('/drafts/<draft_id>', methods=['GET'])
def get_draft(draft_id):
    """Fetches a draft by its ID"""
    draft_data = drafts_collection.find_one({"_id": ObjectId(draft_id)})
    if draft_data:
        hole = Draft(**draft_data)
        return jsonify({
            hole
        })
    return abort(404, description="Draft not found")