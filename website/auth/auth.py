from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import check_password_hash, generate_password_hash
from .. import db
from .models import users
from ..extensions import bcrypt

auth = Blueprint("auth", __name__, static_folder="../static", template_folder="../templates")


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST": 
        email = request.form.get('email')
        password = request.form.get('password')

        found_user = users.query.filter_by(email=email).first() # SQL search query checks if email is in db
        print(f'Found user: {found_user}')  # Debug: Check if user is found

        if found_user: #If email is in db
            print(f'User email: {found_user.email}')  # Debug: Check user email
            print(f'User password hash: {found_user.password}')  # Debug: Check stored password hash
            if check_password_hash(found_user.password, password): # Returns true if inputted figure matchs the unhashed password
                flash("Logged in Successfully!", category='success')
                login_user(found_user, remember=True)
                return redirect(url_for('.user'))
            else:
                flash("Incorrect password, try again.", category='error')
        else:
            flash("Email does not exist.", category='error')

    return render_template("login.html", found_user=current_user)


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST': # When a form is POSTed (i.e. Submitted on user end)
        email = request.form.get('email')
        name = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        existing_user = users.query.filter_by(name=name).first()  # SQL search query checks if name is in db
        if existing_user:
            flash('Email already exists.', category='error')  # Error message if email already exists in db
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')  # Error message if entered email is shorter than 4 characters 
        elif len(name) < 2:
            flash('Name must be greater than 1 character.', category='error')  # Error message if name is shorter than 2 characters
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')  # Error message if passwords from both forms don't match
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')  # Error message if password is shorter than 7 characters
        else:
            print(f'Password during sign-up: {password1}') # Debug: Print entered password
            hashed_password = generate_password_hash(password1).decode('utf-8')  # Hashes password using utf-8 encoding standard
            print(f'Hashed password during sign-up: {hashed_password}')  # Debug: Print hashed password
            new_user = users(email=email, name=name, password=hashed_password, highscore=0)
            db.session.add(new_user)  # Adds user info into db session
            db.session.commit()  # Commits db session data to db
            login_user(new_user, remember=True)  # Adds user to current session i.e "logging them in" (via flask_login)
            flash('Account created!', category='success')
            return redirect(url_for('.user'))

    return render_template("signup.html", user=current_user)

# User route after logging in
@auth.route("/user", methods=["POST", "GET"]) 
@login_required
def user():
    email = current_user.email
    name = current_user.name
    highscore = current_user.highscore
    return render_template("user.html", 
                           email=email, 
                           name=name,
                           highscore=highscore
                           )

# Logout function
@auth.route("/logout")
@login_required
def logout():
    logout_user() # Pops User session Data 
    flash("you have been logged out!", "info") 
    return redirect(url_for(".login")) #redirect to login page
