# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


from .User import User
# from .Profile import Profile
from .Group import Group
from .UserGroup import UserGroup
from .Stats import Stats
from .Match import Match

