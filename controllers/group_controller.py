from flask import request, jsonify, flash, redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from models.Group import Group
from models.User import User
from schemas.group_schema import GroupSchema
from schemas.user_schema import UserSchema
from models.UserGroup import UserGroup
from app import db

group_schema = GroupSchema()
groups_schema = GroupSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)

def get_groups(user):
    groups = [group.to_dict() for group in user.groups if not group.hidden]
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

    db.session.add(group)
    db.session.flush() 

    user_group = UserGroup(user_id=user.id, group_id=group.id, seen=False)
    db.session.add(user_group)
    db.session.commit()

    return jsonify({'message': 'Group created!', 'group': group.to_dict()}), 201


def get_group_by_id(group_id, user):
    group = Group.query.get(group_id)
    if not group:
        return jsonify({'message': 'Group not found'}), 404
    assoc = UserGroup.query.filter_by(user_id=user.id, group_id=group.id).first()
    if not assoc:
        return jsonify({'message': 'User not in group'}), 403
    assoc.seen = True
    db.session.commit()

    return jsonify(group.to_dict()), 200


def hide_group(group_id):
    group = Group.query.get(group_id)
    if not group:
        return jsonify({'message': 'Group not found'}), 404

    group.hidden = True
    db.session.commit()

    return jsonify({'message': 'Group hidden successfully!'}), 200


def check_new_groups(user):
    unseen_groups = (db.session.query(UserGroup).filter_by(user_id=user.id, seen=False).all())
    if not unseen_groups:
        return jsonify({'message': 'No new groups found'}), 200
    return jsonify([group.group.to_dict() for group in unseen_groups]), 200
