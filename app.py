from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from config import Config
import os


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
from models.Stats import Stats
from models.Match import Match

# Importing models, routes, and controllers after initialization
from routes.user_routes import user_routes
# from routes.profile_routes import profile_routes
# from routes.group_routes import group_routes
from routes.stats_routes import stats_routes
from routes.match_routes import match_routes

# Register routes
app.register_blueprint(user_routes)
app.register_blueprint(stats_routes)
app.register_blueprint(match_routes)
# app.register_blueprint(profile_routes)
# app.register_blueprint(group_routes)

DISCORD_CLIENT_ID = '1349024595683967007'
DISCORD_REDIRECT_URI = 'http://localhost:5000/auth/discord/'
DISCORD_CLIENT_SECRET = 'HpJuvqB-gHgUAUT_KcLg1tkRrJN9MY-D'
DISCORD_API_BASE_URL = 'https://discord.com/api'

app.secret_key = "jpdsecret"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem" 

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')

@app.cli.command('discinfo')
def printdiscinfo():
    print(DISCORD_CLIENT_ID)
    print(DISCORD_REDIRECT_URI)
    print(DISCORD_CLIENT_SECRET)
    print(DISCORD_API_BASE_URL)

if __name__ == '__main__':
    app.run()