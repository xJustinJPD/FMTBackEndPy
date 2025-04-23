from app import db
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Float
import json

class Stats(db.Model):
    __tablename__ = 'stats'
    id = Column(Integer, primary_key=True)
    kills = Column(Integer)
    deaths = Column(Integer)
    assists = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    rank = Column(String)
    winloss = Column(Float)
    kda = Column(Float)
    kapm = Column(Float)
    winpercent = Column(Integer)
    last20kills = Column(String)
    last20deaths = Column(String)
    last20assists = Column(String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    user = db.relationship('User', back_populates='stats')

    def to_dict(self):
        return {
            'kills': self.kills,
            'deaths': self.deaths,
            'assists': self.assists,
            'wins': self.wins,
            'losses': self.losses,
            'rank': self.rank,
            'winloss': self.winloss,
            'kda': self.kda,
            'kapm': self.kapm,
            'winpercent': self.winpercent,
            'last20kills': json.loads(self.last20kills) if self.last20kills else [],
            'last20deaths': json.loads(self.last20deaths) if self.last20deaths else [],
            'last20assists': json.loads(self.last20assists) if self.last20assists else [],
        }