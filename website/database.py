# DATABASE CONFIG
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData

# Constraint Naming Convetion - Define a naming convention for database constraints to ensure consistency
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=naming_convention) # Apply naming convention to metadata

# Other DB Config
db = SQLAlchemy(metadata=metadata) # Initialize SQLAlchemy with the defined metadata
migrate = Migrate(db, render_as_batch=True) # Initialize Migrate with batch mode enabled for migrations
