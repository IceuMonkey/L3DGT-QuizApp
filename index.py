from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
from markupsafe import escape

app = Flask(__name__)
app.secret_key = "hello test"
app.permanent_session_lifetime = timedelta(minutes=5) #Will stay logged in for 5 minutes

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
    #if else used to check if user is logged in/ has a session. Renders dynamic url if logged in, returns with login page if not 
    if request.method == "POST": 
        session.permanent = True #Saves session data "permanently" 
        user = request.form["nm"]
        session["user"] = user  
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        
        return render_template("login.html")

# Dynamic routing for user page
@app.route("/user") 
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("login"))

# Logout function
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(debug=True)
# debug=True will automatically rerun the app whe I make a change to the code