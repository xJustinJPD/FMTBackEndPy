from app import db
from sqlalchemy import Column, Integer, String, ForeignKey

class UserGroup(db.Model):
    __tablename__ = 'UserGroup'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    seen = db.Column(db.Boolean, default=False)


    user = db.relationship('User', back_populates='group_associations')
    group = db.relationship('Group', back_populates='user_associations')