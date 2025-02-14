from flask import Blueprint, request
from controllers.user_controller import register, login

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return register(data)

@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login(data)
