from flask import Flask
from flask_login import LoginManager

from .config import Config
from .database import db, migrate
from .extensions import bcrypt, login_manager
from .auth.models import users
from .quiz.models import Question


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Login Manager
    login_manager = LoginManager()
    login_manager.login_view = app.config['LOGIN_VIEW']
    
    # Initialising Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(id):
        return users.query.get(int(id))

    # Registering Blueprints
    from .auth.auth import auth as auth_blueprint
    from .routes import main as main_blueprint
    from .dbroutes import db_bp as db_blueprint
    from .quiz.quiz import quiz_bp as quiz_blueprint
    from .settings import settings_bp as settings_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(quiz_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(db_blueprint)
    app.register_blueprint(settings_blueprint)

    print("Blueprints registered: ", app.blueprints)  # Debug: Print registered blueprints

    return app