from flask import Blueprint, render_template

from .auth.models import users
from .quiz.models import Question

db_bp = Blueprint('db_bp', __name__, static_folder="./static", template_folder="./templates")

# Routes to display database tables
@db_bp.route("/users-db") # Shows users table
def usersdb():
    return render_template("usersdb.html", values=users.query.all()) # Renders template and passes all values queried from user db 

@db_bp.route("/questions-db") # Shows questions table
def questionsdb(): 
    return render_template("questionsdb.html", values=Question.query.all()) # Renders template and passes all values queried from questions db 
