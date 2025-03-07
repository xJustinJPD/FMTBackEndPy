from app import db
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Float

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
            'winpercent': self.winpercent
        }