from flask import Blueprint, request
from controllers.user_controller import register, login, add_user_to_group, get_user, get_users, update_user, delete_user
from flask_jwt_extended import jwt_required

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

@user_routes.route('/user/<int:user_id>', methods=['GET'])
def get_this_user(user_id):
    return get_user(user_id)

@user_routes.route('/users', methods=['GET'])
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
