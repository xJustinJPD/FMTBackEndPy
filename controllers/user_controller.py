from flask import request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from models.User import User
from schemas.user_schema import UserSchema
from app import db

user_schema = UserSchema()
users_schema = UserSchema(many=True)

def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exists', status=409), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
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
        access_token = create_access_token(identity=email)
        return jsonify(message='Login succeeded!', access_token=access_token)
    else:
        return jsonify(message='Bad email or password', status=401), 401
