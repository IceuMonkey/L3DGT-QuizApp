from flask_bcrypt import Bcrypt
from flask_login import LoginManager

bcrypt = Bcrypt() # Initialise Bcrypt instance for password hashing
login_manager = LoginManager() # Initialise LoginManager instance for managing user sessions