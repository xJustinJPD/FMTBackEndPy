from app import db
from sqlalchemy import Column, Integer, String, Table, ForeignKey

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    bio = Column(String)
    role = Column(String)
    groups = db.relationship('Group', secondary='user_group' ,back_populates='users')
    stats = db.relationship('Stats', back_populates='user', uselist=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'bio': self.bio,
            'role': self.role,
            # 'groups': [group.to_dict() for group in self.groups],
            'stats': self.stats.to_dict()
        }
