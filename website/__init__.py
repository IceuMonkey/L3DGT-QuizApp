from flask import Flask

from .config import Config
from .database import db, migrate
from .extensions import bcrypt, login_manager
from .auth.models import users
from .quiz.models import Question


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialising Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Login Manager
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        return users.query.get(int(id))

    # Registering Blueprints
    from .auth.auth import auth as auth_blueprint
    from .routes import main as main_blueprint
    from .quiz.quiz import quiz_bp as quiz_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/")
    app.register_blueprint(quiz_blueprint)
    app.register_blueprint(main_blueprint)

    print("Blueprints registered: ", app.blueprints)  # Debug: Print registered blueprints

    return app