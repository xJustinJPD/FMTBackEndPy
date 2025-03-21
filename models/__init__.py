# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


from .User import User
# from .Profile import Profile
from .Group import Group
from .User_Group import user_group
from .Stats import Stats
from .Match import Match

