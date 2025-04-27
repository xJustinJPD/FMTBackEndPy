import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://findmyteam_user:BaKKK9aZzc10NBDtOgmfvPixoBxctPvx@dpg-d079b72li9vc73f3j350-a.frankfurt-postgres.render.com/findmyteam'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'super-secret'
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = 'c58eaa1cc3b8b0'
    MAIL_PASSWORD = '********4872'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    DISCORD_CLIENT_ID = '1349024595683967007'
    DISCORD_CLIENT_SECRET = 'HpJuvqB-gHgUAUT_KcLg1tkRrJN9MY-D'
    DISCORD_REDIRECT_URI = 'https://fmtbackendpy.onrender.com/auth/discord/'
    DISCORD_API_BASE_URL = 'https://discord.com/api'
    
