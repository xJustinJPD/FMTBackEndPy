from app import db
from sqlalchemy import Column, Integer, String

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    groups = db.relationship('Group', secondary=user_groups ,backref='user', lazy=True)
