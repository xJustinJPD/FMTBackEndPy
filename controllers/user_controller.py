from flask import request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from models.User import User
from models.Group import Group
from schemas.user_schema import UserSchema
from app import db

user_schema = UserSchema()
users_schema = UserSchema(many=True)

def register():
    email = request.form['email']
    username = request.form['username']
    test_username = User.query.filter_by(username=username).first()
    if test_username:
        return jsonify(message='That username already exists', status=409), 409

    test_email = User.query.filter_by(email=email).first()
    if test_email:
        return jsonify(message='That email already exists', status=409), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        role = request.form['role']
        bio = request.form['bio']
        user = User(username=username, first_name=first_name, last_name=last_name, email=email, password=password, role=role, bio=bio)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User created successfully', status=201), 201


def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    user = User.query.filter_by(email=email, password=password).first()
    if user:
        access_token = create_access_token(identity=str(email))
        return jsonify(message='Login succeeded!', access_token=access_token)
    else:
        return jsonify(message='Bad email or password', status=401), 401


def add_user_to_group():
    # Get the data from the request (user_id and group_id)
    user_id = request.json.get('user_id')
    group_id = request.json.get('group_id')

    # Find the user and the group
    user = User.query.get(user_id)
    group = Group.query.get(group_id)

    if not user or not group:
        return jsonify({'message': 'User or Group not found'}), 404

    # Add the user to the group
    user.groups.append(group)
    db.session.commit()

    return jsonify({'message': 'User added to group successfully'}), 200


def get_user(user_id: int):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return jsonify(user.to_dict())
    else:
        return jsonify(message='That user does not exist', status=404), 404
    

def get_users():
    users_list = User.query.all()
    result = [user.to_dict() for user in users_list]
    return jsonify(result)

def update_user(user_id: int):
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.username = request.form['username']
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.bio = request.form['bio']
        user.role = request.form['role']
        user.email = request.form['email']
        user.password = request.form['password']
        db.session.commit()
        return jsonify(message='You updated a profile', status=202), 202
    else:
        return jsonify(message='That profile does not exist', status=404), 404
    

def delete_user(user_id: int):
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(message='You deleted your profile', status=202), 202
    else:
        return jsonify(message='That profile does not exist', status=404), 404
