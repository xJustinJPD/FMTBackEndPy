import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'planets.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'super-secret'  # Change this!
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = 'c58eaa1cc3b8b0'
    MAIL_PASSWORD = '********4872'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
