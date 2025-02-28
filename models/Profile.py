# from app import db
# from sqlalchemy import Column, Integer, String

# class Profile(db.Model):
#     __tablename__ = 'profile'
#     profile_id = Column(Integer, primary_key=True)
#     profile_fname = Column(String)
#     profile_lname = Column(String)
#     role = Column(String)
#     bio = Column(String)
#     user_id = Column(Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
#     user = db.relationship('User', back_populates='profile')

#     def to_dict(self):
#         return {
#             'profile_id': self.profile_id,
#             'profile_fname': self.profile_fname,
#             'profile_lname': self.profile_lname,
#             'role': self.role,
#             'bio': self.bio,
#             'user_id': self.user_id
#         }