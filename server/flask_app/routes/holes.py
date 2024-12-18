from flask import jsonify, abort, Blueprint
import sys
import os
from bson.objectid import ObjectId

# Adjust the paths for MacOS to get the flask_app directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db
from models import Hole

holes_collection = db.holes
holes_bp = Blueprint('holes', __name__)


@holes_bp.route('/holes/<hole_id>', methods=['GET'])
def get_hole(hole_id):
    """Fetches a hole by ID"""
    hole_data = holes_collection.find_one({"_id": ObjectId(hole_id)})
    if hole_data:
        hole = Hole(**hole_data)
        return jsonify({
            hole
        })
    return abort(404, description="Hole not found")