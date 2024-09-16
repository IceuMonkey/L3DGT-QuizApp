from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from datetime import timedelta
from markupsafe import escape
from sqlalchemy import MetaData

#Blueprints
from second import second

# Config Stuff
app = Flask(__name__)
app.register_blueprint(second, url_prefix="admin")

app.secret_key = "hjkhkjhkjkjh" # key for session
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Removes warning when database if is modified
app.permanent_session_lifetime = timedelta(minutes=5) #Will stay logged in for 5 minutes after closing app

### DATABASE
# Constraint Naming Convetion
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=naming_convention)

# Config
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)
# Schema
class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True) 
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(150), unique=True)
    highscore = db.Column("highscore", db.Integer, db.CheckConstraint('highscore >= 0', name='check_highscore_positive'))
    
    __table_args__ = (
        db.UniqueConstraint('name', name='uq_user_name'),
        db.UniqueConstraint('email', name='uq_user_email'),
        db.UniqueConstraint('highscore', name='uq_user_highscore'),
    )

    def __init__(self, name, email, highscore):
        self.name = name
        self.email = email
        self.highscore = highscore

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
    session.pop("highscore", None)
    #redirect to login page
    return redirect(url_for("login"))

# Page to display database
@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())


if __name__ == "__main__":
    with app.app_context(): 
        db.create_all() # Initialises DB on start up before running app
    app.run(debug=True) # debug=True will automatically rerun the app whe I make a change to the code