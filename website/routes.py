from flask import Blueprint, render_template

# Create main blueprint
main = Blueprint('main', __name__)

# Basic App route (Index Page)
@main.route("/")
def index():
    return render_template("index.html")
