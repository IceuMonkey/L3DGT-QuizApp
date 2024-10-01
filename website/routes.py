from flask import Blueprint, render_template
from .auth.models import users

main = Blueprint('main', __name__)

# Basic App route
@main.route("/")
def index():
    return render_template("index.html")


# Routes to display databases
@main.route("/users-db")
def view():
    return render_template("usersdb.html", values=users.query.all())

