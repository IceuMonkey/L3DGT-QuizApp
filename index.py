from flask import Flask, redirect, url_for, render_template
from markupsafe import escape
app = Flask(__name__)

# Basic App route
@app.route("/")
def index():
    return render_template("index.html")

# Second App route 
@app.route("/quiz")
def quizlist():
    return render_template("quiz.html")

# Dynamic routing using 
@app.route("/user/<username>") 
def show_user(username):
    return f'Hello {username}'


if __name__ == "__main__":
    app.run(debug=True)
# debug=True will automatically rerun the app whe I make a change to the code