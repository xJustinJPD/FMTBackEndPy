import requests
from flask import request, jsonify, session
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from models.Match import Match
from models.User import User
from schemas.match_schema import MatchSchema
from app import db, app

match_schema = MatchSchema()
match_schema = MatchSchema(many=True)

def send_like(liked_id, user):
    existmatch = Match.query.filter_by(liker_id=user.id, liked_id=liked_id).first()
    if existmatch:
        return jsonify({'message': 'You liked this user already'}), 400
    
    match = Match(liker_id=user.id, liked_id=liked_id)
    db.session.add(match)
    db.session.commit()

    return jsonify({'message': f'Like sent by: {user.id}'}), 201


def get_likes(user):
    matches = Match.query.filter_by(liker_id=user.id, status="pending").all()
    result = [match.to_dict() for match in matches]
    return jsonify(result), 200


def respond_to_like(match_id):
    match = Match.query.filter_by(id=match_id, status="pending").first()

    if not match:
        return jsonify({'message': 'No like found'}), 404
    
    status = request.json.get('status').lower()

    if status not in ['accepted', 'rejected']:
        return jsonify({'message': 'Invalid status'}), 400
    
    match.status = status
    db.session.commit()
    return jsonify({'message': f'Match {status}'}), 200