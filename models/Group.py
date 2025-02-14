from app import db
from sqlalchemy import Column, Integer, String

class Group(db.Model):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    group_name = Column(String)
    users = db.relationship('User', backref='group', lazy=True)