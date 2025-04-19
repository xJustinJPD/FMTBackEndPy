from flask import Blueprint, request, jsonify
from controllers.group_controller import create_group, get_groups, get_group_by_id, hide_group
from models.User import User 
from flask_jwt_extended import jwt_required, get_jwt_identity

group_routes = Blueprint('group_routes', __name__)

@group_routes.route('/groups', methods=['GET'])
@jwt_required()
def get_groups_route():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'message': 'User not found'}), 404
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return get_groups(user)


@group_routes.route('/groups', methods=['POST'])
@jwt_required()
def create_group_route():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'message': 'User not found'}), 404
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return create_group(user)


@group_routes.route('/groups/<int:group_id>', methods=['GET'])
@jwt_required()
def get_group_by_id_route(group_id):
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'message': 'User not found'}), 404
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return get_group_by_id(group_id)


@group_routes.route('/groups/<int:group_id>/delete', methods=['PUT'])
@jwt_required()
def hide_group_route(group_id):
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'message': 'User not found'}), 404
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return hide_group(group_id)