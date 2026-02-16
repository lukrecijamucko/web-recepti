import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
    DB_PATH = os.environ.get("DB_PATH", "instance/app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
