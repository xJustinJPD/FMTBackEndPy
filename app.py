# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import Column, Integer, String, Float
# from flask_marshmallow import Marshmallow
# from flask_jwt_extended import JWTManager, jwt_required, create_access_token
# from flask_mail import Mail, Message
# from flask_cors import CORS
# import os
# from models.Planet import Planet
# from models.User import User
# from models.Profile import Profile
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)
CORS(app)

user_groups = db.Table('user_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)


# Importing models, routes, and controllers after initialization
from routes.user_routes import user_routes
from routes.profile_routes import profile_routes
from routes.group_routes import group_routes

# Register routes
app.register_blueprint(user_routes)
app.register_blueprint(profile_routes)
app.register_blueprint(group_routes)


# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
# app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
# app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
# app.config['MAIL_PORT'] = 2525
# app.config['MAIL_USERNAME'] = 'c58eaa1cc3b8b0'
# app.config['MAIL_PASSWORD'] = '********4872'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False


# CORS(app)
# db = SQLAlchemy(app)
# ma = Marshmallow(app)
# jwt = JWTManager(app)
# mail = Mail(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')

# @app.cli.command('db_seed')
# def db_seed():
#         test_user = User(first_name='Justin',
#                         last_name='Perry-Doyle',
#                         email = 'justin@email.com',
#                         password = 'password')

#         test_profile = Profile(profile_fname='Justin',
#                         profile_lname='Perry-Doyle',
#                         role = 'Controller',
#                         bio = 'Hi I am Justin, I am a controller')
#         test_profile2 = Profile(profile_fname='Kacper',
#                         profile_lname='Agatowski',
#                         role = 'Duelist',
#                         bio = 'Hi I am Kacper, I am a duelist')
#         db.session.add(test_profile2)
#         db.session.add(test_profile)
#         db.session.add(test_user)
#         db.session.commit()
#         print('Database seeded!')


# @app.route('/notfound')
# def not_found():
#     return jsonify(message='Resource not found', status=404), 404


# Profiles Routes
# @app.route('/profiles', methods=['GET'])
# def profiles():
#     profiles_list = Profile.query.all()
#     result = profiles_schema.dump(profiles_list)
#     return jsonify(result)


# @app.route('/profile/<int:profile_id>', methods=['GET'])
# def profile(profile_id: int):
#     profile = Profile.query.filter_by(profile_id=profile_id).first()
#     if profile:
#         result = profile_schema.dump(profile)
#         return jsonify(result)
#     else:
#         return jsonify(message='That profile does not exist', status=404), 404


# @app.route('/add_profile', methods=['POST'])
# @jwt_required()
# def add_profile():
#     profile_fname = request.form['profile_fname']
#     test = Profile.query.filter_by(profile_fname=profile_fname).first()
#     if test:
#         return jsonify(message='There is already a profile by that name', status=409), 409
#     else:
#         profile_lname = request.form['profile_lname']
#         role = request.form['role']
#         bio = request.form['bio']
#         profile = Profile(profile_fname=profile_fname, profile_lname=profile_lname, role=role, bio=bio)
#         db.session.add(profile)
#         db.session.commit()
#         return jsonify(message='You added a profile', status=201), 201


# @app.route('/update_profile/<int:profile_id>', methods=['PUT'])
# @jwt_required()
# def update_profile(profile_id: int):
#     profile = Profile.query.filter_by(profile_id=profile_id).first()
#     if profile:
#         profile.profile_fname = request.form['profile_fname']
#         profile.profile_lname = request.form['profile_lname']
#         profile.role = request.form['role']
#         profile.bio = request.form['bio']
#         db.session.commit()
#         return jsonify(message='You updated a profile', status=202), 202
#     else:
#         return jsonify(message='That profile does not exist', status=404), 404


# @app.route('/delete_profile/<int:profile_id>', methods=['DELETE'])
# @jwt_required()
# def delete_profile(profile_id: int):
#     profile = Profile.query.filter_by(profile_id=profile_id).first()
#     if profile:
#         db.session.delete(profile)
#         db.session.commit()
#         return jsonify(message='You deleted a profile', status=202), 202
#     else:
#         return jsonify(message='That profile does not exist', status=404), 404


# @app.route('/register', methods=['POST'])
# def register():
#     email = request.form['email']
#     test = User.query.filter_by(email=email).first()
#     if test:
#         return jsonify(message='That email already exists', status=409), 409
#     else:
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         password = request.form['password']
#         user = User(first_name=first_name, last_name=last_name, email=email, password=password)
#         db.session.add(user)
#         db.session.commit()
#         return jsonify(message='User created successfully', status=201), 201


# @app.route('/login', methods=['POST'])
# def login():
#     if request.is_json:
#         email = request.json['email']
#         password = request.json['password']
#     else:
#         email = request.form['email']
#         password = request.form['password']

#     user = User.query.filter_by(email=email, password=password).first()
#     if user:
#         access_token = create_access_token(identity=email)
#         return jsonify(message='Login succeeded!', access_token=access_token)
#     else:
#         return jsonify(message='Bad email or password', status=401), 401



# DB Models
# class User(db.Model):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     first_name = Column(String)
#     last_name = Column(String)
#     email = Column(String, unique=True)
#     password = Column(String)


# class Profile(db.Model):
#     __tablename__ = 'profiles'
#     profile_id = Column(Integer, primary_key=True)
#     profile_fname = Column(String)
#     profile_lname = Column(String)
#     role = Column(String)
#     bio = Column(String)

#Schemas
# class UserSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'first_name', 'last_name', 'email', 'password')


# class ProfileSchema(ma.Schema):
#     class Meta:
#         fields = ('profile_id', 'profile_fname', 'profile_lname', 'role', 'bio')


# #Enstantiate the schemas
# user_schema = UserSchema()
# users_schema = UserSchema(many=True)


# profile_schema = ProfileSchema()
# profiles_schema = ProfileSchema(many=True)



if __name__ == '__main__':
    app.run()