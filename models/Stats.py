from app import db
from sqlalchemy import Column, Integer, String, Table, ForeignKey

class Stats(db.Model):
    __tablename__ = 'stats'
    id = Column(Integer, primary_key=True)
    kills = Column(Integer)
    deaths = Column(Integer)
    assists = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    rank = Column(String)

    def to_dict(self):
        return {
        }