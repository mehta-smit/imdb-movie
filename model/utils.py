"""
Helper Utility functionalities for Model Declarations
"""

from sqlalchemy import Column, text

from .base import db

PRIMARY_KEY = Column(db.Integer, primary_key=True, autoincrement=True)
CREATED_AT = Column(db.DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

MODIFIED_AT = Column(db.DateTime, nullable=False, server_default=text(
    "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

IS_DELETED = Column(db.SmallInteger, server_default=text('0'))
