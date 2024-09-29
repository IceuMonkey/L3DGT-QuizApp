from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import db, bcrypt
from .models import users

auth = Blueprint("auth", __name__, static_folder="static", template_folder="templates")

# GET & POST methods from form
@auth.route("/login", methods=["POST", "GET"])
def login():
    #if else used to check if user is logged in/ has a session. Renders /user if logged in, returns with login page if not 
    if request.method == "POST": 
        email = request.form.get('email')
        password = request.form.get('password')

        found_user = users.query.filter_by(email=email).first() #SQL search query checks if email is in db
        if found_user: # If user is in db
            if bcrypt.check_password_hash(user.passsword, password): # If password is correct
                flash("Logged in Successfully!", category='success')
                login_user(user, remember=True) # Adds user to current session i.e "logging them in" (via flask_login)
                return redirect(url_for('views.home'))
            else: # If password is incorrect
                flash("Incorrect, try again.", category='error')
        else: # User doesn't exist in db
            flash("Email does not exist.", category='error')


        flash("Login Successful!")
        return render_template("login.html", found_user=current_user)

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        existing_user = users.query.filter_by(name=name).first() #SQL search query checks if name is in db
        if existing_user:
            flash('Email already exists.', category='error') # Error message if email already exists in db
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error') # Error message if entered email is shorter than 4 characters 
        elif len(name) < 2:
            flash('Name must be greater than 1 character.', category='error') # Error message if name is shorter than 2 characters
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error') # Error message if passwords from both forms don't match
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error') # Error message if password is shorter than 7 characters
        else:
            hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8') # Hashes password using utf-8 encoding standard
            new_user = users(email=email, name=name, password=hashed_password, highscore=0)
            db.session.add(new_user) # Adds user info into db session
            db.session.commit() # Commits db session data to db
            login_user(new_user, remember=True) # Adds user to current session i.e "logging them in" (via flask_login)
            flash('Account created!', category='success')
            return redirect(url_for('.users'))

    return render_template("signup.html", user=current_user)


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
@login_required
def logout():
    logout_user()    
    #redirect to login page
    return redirect(url_for("auth.login"))
