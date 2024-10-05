from flask import Blueprint, render_template

main = Blueprint('main', __name__)

# Basic App route
@main.route("/")
def index():
    return render_template("index.html")
