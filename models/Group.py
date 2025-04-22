from app import db
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Boolean

class Group(db.Model):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    group_name = Column(String)
    hidden = Column(Boolean, default=False)
    user_associations = db.relationship('UserGroup', back_populates='group', lazy='dynamic')
    users = db.relationship('User', secondary='UserGroup', viewonly=True)

    def to_dict(self):
        return {
            'id': self.id,
            'group_name': self.group_name,
            'users': [user.to_dict_no_groups() for user in self.users]
        }