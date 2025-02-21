from app import db
from sqlalchemy import Column, Integer, String, Table, ForeignKey

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    groups = db.relationship('Group', secondary='user_group' ,backref='user')

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'groups': [group.id for group in self.groups]
        }
