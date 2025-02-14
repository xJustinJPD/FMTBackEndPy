from app import db
from sqlalchemy import Column, Integer, String

class Profile(db.Model):
    __tablename__ = 'profiles'
    profile_id = Column(Integer, primary_key=True)
    profile_fname = Column(String)
    profile_lname = Column(String)
    role = Column(String)
    bio = Column(String)
