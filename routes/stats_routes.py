from flask import Blueprint, request
from controllers.stats_controller import get_matches, get_match, get_stats
from flask_jwt_extended import jwt_required

stats_routes = Blueprint('stats_routes', __name__)

@stats_routes.route('/matches', methods=['GET'])
def get_matches_route():
    return get_matches()

@stats_routes.route('/match', methods=['GET'])
def get_match_route():
    return get_match()

@stats_routes.route('/stats', methods=['POST'])
def get_stats_route():
    return get_stats()

