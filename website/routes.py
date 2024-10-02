from flask import Blueprint, render_template
from .auth.models import users
from .quiz.models import Question

main = Blueprint('main', __name__)

# Basic App route
@main.route("/")
def index():
    return render_template("index.html")


# Routes to display databases
@main.route("/users-db")
def usersdb():
    return render_template("usersdb.html", values=users.query.all())

@main.route("/questions-db")
def questionsdb():
    return render_template("questionsdb.html", values=Question.query.all())

