# USERS DB
from flask_login import UserMixin

from ..database import db

# DB Schema
class users(db.Model, UserMixin):
    id = db.Column("id", db.Integer, primary_key=True) 
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(150), unique=True) # Must be Unique
    password = db.Column("password", db.String, nullable=False)
    highscore = db.Column("highscore", db.Integer, db.CheckConstraint('highscore >= 0', name='check_highscore_positive'))
    
    __table_args__ = (
        db.UniqueConstraint('name', name='uq_user_name'),
        db.UniqueConstraint('email', name='uq_user_email'),
    )

    def __init__(self, name, email, password, highscore):
        self.name = name
        self.email = email
        self.password = password
        self.highscore = highscore
