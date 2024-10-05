from flask import Blueprint, render_template

from .auth.models import users
from .quiz.models import Question

db_bp = Blueprint('db_bp', __name__, static_folder="./static", template_folder="./templates")

# Routes to display databases
@db_bp.route("/users-db")
def usersdb():
    return render_template("usersdb.html", values=users.query.all()) 

@db_bp.route("/questions-db")
def questionsdb():
    return render_template("questionsdb.html", values=Question.query.all())
