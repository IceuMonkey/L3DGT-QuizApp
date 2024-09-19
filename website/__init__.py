from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from datetime import timedelta
from sqlalchemy import MetaData


# Config Stuff
app = Flask(__name__)

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

# Other DB Config
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)

#Blueprints
from .models import users
from .auth import auth as auth_blueprint
from .routes import main as main_blueprint

app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(main_blueprint)