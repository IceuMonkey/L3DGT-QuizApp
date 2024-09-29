from flask import Blueprint, render_template
from .models import users

main = Blueprint('main', __name__)

# Basic App route
@main.route("/")
def index():
    return render_template("index.html")

# Second App route 
@main.route("/quiz")
def quizlist():
    return render_template("quiz.html")


# Page to display database
@main.route("/viewdb")
def view():
    return render_template("viewdb.html", values=users.query.all())

