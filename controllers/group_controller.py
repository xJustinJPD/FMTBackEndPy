from flask import request, jsonify, flash, redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from models.Group import Group
from models.User import User
from schemas.group_schema import GroupSchema
from schemas.user_schema import UserSchema
from app import db

group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

def get_groups(user):
    groups = [group.to_dict() for group in user.groups]
    if not groups:
        return jsonify({'message': 'No groups found'}), 404 
    return jsonify(groups), 200

def create_group(user):
    data = request.get_json()
    group_name = data.get('group_name')

    if not group_name:
        return jsonify({'message': 'Group name is required'}), 400

    # Create group and add creator
    group = Group(group_name=group_name)
    group.users.append(user)

    db.session.add(group)
    db.session.commit()

    return jsonify({'message': 'Group created!', 'group': group.to_dict()}), 201
