from ..database import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    options = db.Column(db.PickleType, nullable=False)  # Store options as a list of 4 items

