from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from . import db
from .models import users

auth = Blueprint("auth", __name__, static_folder="static", template_folder="templates")

# GET & POST methods from form
@auth.route("/login", methods=["POST", "GET"])
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
            usr = users(name=user, email="", highscore=0) 
            db.session.add(usr)
            db.session.commit()


        flash("Login Successful!")
        return redirect(url_for("auth.user"))
    else:
        if "user" in session:
            flash("Already Logged in")
            return redirect(url_for("auth.user"))
        
        return render_template("login.html")

# User route after logging in
@auth.route("/user", methods=["POST", "GET"]) 
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
        return redirect(url_for("auth.login"))

# Logout function
@auth.route("/logout")
def logout():
    if "user" in session:
        user = session["user"] 
        flash("you have been logged out!", "info") 
    # Clears session data
    session.pop("user", None) 
    session.pop("email", None)
    session.pop("highscore", None)
    #redirect to login page
    return redirect(url_for("auth.login"))
