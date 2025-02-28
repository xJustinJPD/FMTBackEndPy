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

# with app.app_context():
#     db.session.execute('PRAGMA foreign_keys=ON')

from models.User import User
# from models.Profile import Profile
from models.Group import Group
from models.User_Group import user_group

# Importing models, routes, and controllers after initialization
from routes.user_routes import user_routes
# from routes.profile_routes import profile_routes
# from routes.group_routes import group_routes

# Register routes
app.register_blueprint(user_routes)
# app.register_blueprint(profile_routes)
# app.register_blueprint(group_routes)


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
        
#         test_group = Group(group_name='Test Group')


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
#         db.session.add(test_group)
#         db.session.commit()
#         print('Database seeded!')



if __name__ == '__main__':
    app.run()