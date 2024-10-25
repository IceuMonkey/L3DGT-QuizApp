# GENERAL CONFIG
from datetime import timedelta


class Config:
    SECRET_KEY = "hjkhkjhkjkjh" # session key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.sqlite3' # URI used for DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Removes warning when database if is modified (will occur whenever new data is commited)
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=5) # Will keep data in session for 5 minutes after closing app
    LOGIN_VIEW = 'auth.login'