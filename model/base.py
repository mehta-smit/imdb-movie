from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()
migrate = Migrate()
Base = declarative_base()
metadata = Base.metadata

