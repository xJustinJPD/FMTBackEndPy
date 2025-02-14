from flask import request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from models.Profile import Profile
from schemas.profile_schema import ProfileSchema
from app import db

profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)

def get_profiles():
    profiles_list = Profile.query.all()
    result = profiles_schema.dump(profiles_list)
    return jsonify(result)

def get_profile(profile_id: int):
    profile = Profile.query.filter_by(profile_id=profile_id).first()
    if profile:
        result = profile_schema.dump(profile)
        return jsonify(result)
    else:
        return jsonify(message='That profile does not exist', status=404), 404
    

def add_profile():
    profile_fname = request.form['profile_fname']
    test = Profile.query.filter_by(profile_fname=profile_fname).first()
    if test:
        return jsonify(message='There is already a profile by that name', status=409), 409
    else:
        profile_lname = request.form['profile_lname']
        role = request.form['role']
        bio = request.form['bio']
        profile = Profile(profile_fname=profile_fname, profile_lname=profile_lname, role=role, bio=bio)
        db.session.add(profile)
        db.session.commit()
        return jsonify(message='You added a profile', status=201), 201
    

def update_profile(profile_id: int):
    profile = Profile.query.filter_by(profile_id=profile_id).first()
    if profile:
        profile.profile_fname = request.form['profile_fname']
        profile.profile_lname = request.form['profile_lname']
        profile.role = request.form['role']
        profile.bio = request.form['bio']
        db.session.commit()
        return jsonify(message='You updated a profile', status=202), 202
    else:
        return jsonify(message='That profile does not exist', status=404), 404
    

def delete_profile(profile_id: int):
    profile = Profile.query.filter_by(profile_id=profile_id).first()
    if profile:
        db.session.delete(profile)
        db.session.commit()
        return jsonify(message='You deleted a profile', status=202), 202
    else:
        return jsonify(message='That profile does not exist', status=404), 404
