from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy

# Config Stuff
app = Flask(__name__)
app.secret_key = "hello test" # key for session
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Removes warning when database if is modified
app.permanent_session_lifetime = timedelta(minutes=5) #Will stay logged in for 5 minutes after closing app

# DATABASE
db = SQLAlchemy(app)
class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True) 
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))
    
    def __init__(self, name, email):
        self.name = name
        self.email = email

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
    #if else used to check if user is logged in/ has a session. Renders /user if logged in, returns with login page if not 
    if request.method == "POST": 
        session.permanent = True #Saves session data for permanent amount of time (declared in config section) 
        user = request.form["nm"]
        session["user"] = user  

        found_user = users.query.filter_by(name=user).first() #SQL search query
        if found_user:
            session["email"] = found_user.email # Sets user session email what is found in DB
        else: # Commits the username as a new row in the DB 
            usr = users(user, "") 
            db.session.add(usr)
            db.session.commit()


        flash("Login Successful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already Logged in")
            return redirect(url_for("user"))
        
        return render_template("login.html")

# User route after logging in
@app.route("/user", methods=["POST", "GET"]) 
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST": 
            email = request.form["email"]
            session["email"] = email

            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was Saved!")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email=email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

# Logout function
@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"] 
        flash("you have been logged out!", "info") 
    # Clears session data
    session.pop("user", None) 
    session.pop("email", None)
    return redirect(url_for("login"))

# Page to display database
@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())


if __name__ == "__main__":
    with app.app_context(): 
        db.create_all() # Initialises DB on start up before running app
    app.run(debug=True) # debug=True will automatically rerun the app whe I make a change to the code