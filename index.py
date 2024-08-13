from flask import Flask, redirect, url_for, render_template
from flask_bycrypt import Bcrypt
from markupsafe import escape
app = Flask(__name__)

# Basic App route
@app.route("/")
def index():
    return render_template("index.html")

# Second App route 
@app.route("/quizlist")
def quizlist():
    return render_template("list.html")

# Dynamic routing using 
@app.route("/user/<username>") 
def show_user(username):
    return f'Hello {username}'

if __name__ == "__main__":
    app.run()