from flask import Blueprint, request, jsonify, session
from controllers.user_controller import register, login, add_user_to_group, get_user, get_users, update_user, delete_user, discord_login, discord_callback
from models.User import User  # Import the User model
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import decode_token 

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['POST'])
def register_route():
    return register()

@user_routes.route('/login', methods=['POST'])
def login_route():
    return login()

@user_routes.route('/add_user_to_group', methods=['POST'])
def add_user_to_group_route():
    return add_user_to_group()

@user_routes.route('/profile', methods=['GET'])
@jwt_required()
def get_this_user():
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'message': 'User not found'}), 404
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return get_user(user)

@user_routes.route('/users', methods=['POST'])
def get_this_users():
    return get_users()

@user_routes.route('/update_user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_this_user(user_id):
    return update_user(user_id)

@user_routes.route('/delete_user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_this_user(user_id):
    return delete_user(user_id)


@user_routes.route('/discord_login', methods=['GET'])
def discord_login_route():
    token = request.args.get('token')
    if not token:
        return jsonify({'message': 'Missing token'}), 401
    session['token'] = token
    return discord_login()

@user_routes.route('/discord_callback', methods=['GET'])
def discord_callback_route():
    token = session.get('token')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    try:
        decoded = decode_token(token)
        user_id = decoded['sub']
        user = User.query.get(user_id)
    except Exception:
        return jsonify({'message': 'Invalid token'}), 401

    if not user:
        return jsonify({'message': 'User not found'}), 404

    return discord_callback(user)