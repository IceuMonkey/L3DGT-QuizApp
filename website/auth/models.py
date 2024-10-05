# USERS DB
from flask_login import UserMixin

from ..database import db

# DB Schema
class users(db.Model, UserMixin):
    id = db.Column("id", db.Integer, primary_key=True) 
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(150), unique=True) # Must be Unique
    password = db.Column("password", db.String, nullable=False)
    best_streak = db.Column("best_streak", db.Integer, db.CheckConstraint('best_streak >= 0', name='check_best_streak_positive'))
    total_solved = db.Column("total_solved", db.Integer, db.CheckConstraint('total_solved >= 0', name='check_total_solved_positive'), default=0)

    __table_args__ = (
        db.UniqueConstraint('name', name='uq_user_name'),
        db.UniqueConstraint('email', name='uq_user_email'),
    )

    def __init__(self, name, email, password, best_streak=0, total_solved=0):
        self.name = name
        self.email = email
        self.password = password
        self.best_streak = best_streak
        self.total_solved = total_solved
