from flask import Blueprint, request
from controllers.match_controller import send_like, get_likes, respond_to_like
from flask_jwt_extended import jwt_required

match_routes = Blueprint('match_routes', __name__)


@match_routes.route('/like/<int:liked_id>', methods=['POST'])
@jwt_required()
def send_like_route(liked_id):
    return send_like(liked_id)


@match_routes.route('/likes', methods=['GET'])
@jwt_required()
def get_likes_route():
    return get_likes()


@match_routes.route('/like/<int:match_id>', methods=['PUT'])
@jwt_required()
def respond_to_like_route(match_id):
    return respond_to_like(match_id)