from sqlalchemy import Column, Index, text

from .base import db
from .utils import PRIMARY_KEY, CREATED_AT, MODIFIED_AT, IS_DELETED


class User(db.Model):
    __tabelname__ = "user"
    __table_args__ = (
        Index('user_role', 'id', 'user_role'),
        Index('uq_user', 'user_name', 'email', unique=True)
    )

    id = PRIMARY_KEY.copy()
    user_name = Column(db.String(255), index=True)
    email = Column(db.String(255), index=True, unique=True)
    password = Column(db.String(255))
    user_role = Column(db.Integer, index=True)
    pwd_attempt = Column(db.Integer, server_default=text('0'))
    created_at = CREATED_AT.copy()
    modified_at = MODIFIED_AT.copy()
    is_deleted = IS_DELETED.copy()


class UserRole(db.Model):
    __tabelname__ = "user_role"

    id = PRIMARY_KEY.copy()
    role_name = Column(db.String(255))
    created_at = CREATED_AT.copy()
    modified_at = MODIFIED_AT.copy()
    is_deleted = IS_DELETED.copy()


class Permission(db.Model):
    __tablename__ = "permission"

    id = PRIMARY_KEY.copy()
    name = Column(db.String(255))
    created_at = CREATED_AT.copy()
    modified_at = MODIFIED_AT.copy()
    is_deleted = IS_DELETED.copy()


class RolePermission(db.Model):
    __tabelname__ = "role_permission"

    id = PRIMARY_KEY.copy()
    user_role_id = Column(db.Integer)
    permission_id = Column(db.Integer)
    created_at = CREATED_AT.copy()
    is_deleted = IS_DELETED.copy()
