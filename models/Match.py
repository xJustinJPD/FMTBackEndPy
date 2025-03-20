from app import db
from sqlalchemy import Column, Integer, String, Table, ForeignKey, Float
from datetime import datetime

class Match(db.Model):
    __tablename__ = 'match'
    id = Column(Integer, primary_key=True)
    liker_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    liked_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    status = Column(String, default="pending") #Other values are "accepted" and "rejected"
    timestamp = Column(datetime, default=datetime.now)
    liker = db.relationship('User', foreign_keys=[liker_id], backref='likes_sent')
    liked = db.relationship('User', foreign_keys=[liked_id], backref='likes_received')

    def to_dict(self):
        return {
        }