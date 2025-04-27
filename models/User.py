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
    discord_id = Column(String ,nullable=True)
    riot_name = Column(String ,nullable=True)
    riot_tag = Column(String ,nullable=True)
    riot_puuid = Column(String ,nullable=True)
    riot_region = Column(String ,nullable=True)
    rank = Column(String ,nullable=True)
    group_associations = db.relationship('UserGroup', back_populates='user', lazy='dynamic')
    groups = db.relationship('Group', secondary='UserGroup', viewonly=True)
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
            'riot_puuid': self.riot_puuid,
            'rank': self.rank,
            'riot_name': self.riot_name,
            'riot_tag': self.riot_tag,
            'discord_id': self.discord_id,
            'groups': [group.to_dict() for group in self.groups],
            'stats': self.stats.to_dict()
        }
    
    def to_dict_no_groups(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'bio': self.bio,
            'role': self.role,
            'discord_id': self.discord_id,
            'riot_name': self.riot_name,
            'riot_tag': self.riot_tag,
            'riot_puuid': self.riot_puuid,
            'rank': self.rank
        }
