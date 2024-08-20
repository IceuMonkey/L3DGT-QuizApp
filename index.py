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

# # Admin routing
# @app.route("/admin")
# def admin():
#     return redirect(url_for("user", name="Admin!"))

if __name__ == "__main__":
    app.run()