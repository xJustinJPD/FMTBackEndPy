from app import db
from sqlalchemy import Column, Integer, String, Table, ForeignKey

class Group(db.Model):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    group_name = Column(String)
    users = db.relationship('User', secondary='user_group', backref='group')

    def to_dict(self):
        return {
            'id': self.id,
            'group_name': self.group_name,
            'users': [user.id for user in self.users]
        }