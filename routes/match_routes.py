from flask import Blueprint, request, jsonify
from controllers.match_controller import send_like, get_likes, respond_to_like
from models.User import User 
from flask_jwt_extended import jwt_required, get_jwt_identity

match_routes = Blueprint('match_routes', __name__)


@match_routes.route('/like/<int:liked_id>', methods=['POST'])
@jwt_required()
def send_like_route(liked_id):
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'message': 'User not found'}), 404
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return send_like(liked_id, user)


@match_routes.route('/likes', methods=['GET'])
@jwt_required()
def get_likes_route():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'message': 'User not found'}), 404
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return get_likes(user)


@match_routes.route('/like/<int:match_id>', methods=['PUT'])
@jwt_required()
def respond_to_like_route(match_id):
    return respond_to_like(match_id)