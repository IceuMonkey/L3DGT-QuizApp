from . import db

# DB Schema
class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True) 
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(150), unique=True)
    highscore = db.Column("highscore", db.Integer, db.CheckConstraint('highscore >= 0', name='check_highscore_positive'))
    
    __table_args__ = (
        db.UniqueConstraint('name', name='uq_user_name'),
        db.UniqueConstraint('email', name='uq_user_email'),
        db.UniqueConstraint('highscore', name='uq_user_highscore'),
    )

    def __init__(self, name, email, highscore):
        self.name = name
        self.email = email
        self.highscore = highscore
