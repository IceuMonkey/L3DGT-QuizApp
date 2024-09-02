from flask import Flask, redirect, url_for, render_template, request
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

# GET & POST methods from form
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST": 
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")

# Dynamic routing using 
@app.route("/<usr>") 
def user(usr):
    return f"<h1>{usr}</h1>"


if __name__ == "__main__":
    app.run(debug=True)
# debug=True will automatically rerun the app whe I make a change to the code