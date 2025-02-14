from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from controllers.profile_controller import get_profiles, get_profile, add_profile, update_profile, delete_profile

profile_routes = Blueprint('profile_routes', __name__)

@profile_routes.route('/profiles', methods=['GET'])
def get_this_profiles():
    return get_profiles()

@profile_routes.route('/profile/<int:profile_id>', methods=['GET'])
def get_this_profile(profile_id):
    return get_profile(profile_id)

@profile_routes.route('/add_profile', methods=['POST'])
@jwt_required()
def add_this_profile():
    return add_profile()

@profile_routes.route('/update_profile/<int:profile_id>', methods=['PUT'])
@jwt_required()
def update_this_profile(profile_id):
    return update_profile(profile_id)

@profile_routes.route('/delete_profile/<int:profile_id>', methods=['DELETE'])
@jwt_required()
def delete_this_profile(profile_id):
    return delete_profile(profile_id)
