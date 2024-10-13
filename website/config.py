# GENERAL CONFIG
from datetime import timedelta


class Config:
    SECRET_KEY = "hjkhkjhkjkjh" # key for session
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Removes warning when database if is modified
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=5) # Will keep data in session for 5 minutes after closing app
    LOGIN_VIEW = 'auth.login'