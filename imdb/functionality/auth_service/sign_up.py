import json

from flask import current_app as app
from flask_jwt_extended import create_access_token, create_refresh_token

from model import User, UserRole, session, RolePermission, Permission
from utils.common_utils import encrypt
from constant.common_constant import ADMIN_USER, STANDARD_USER, USER_ROLE, ACTIVE


def sign_up(**kwargs):
    def _is_first_user():
        user_count = session.query(User).count()
        if user_count > 0:
            return False
        return True

    def _add_user():
        user_obj = User()
        user_obj.user_name = kwargs.get("user_name")
        user_obj.email = kwargs.get("email")
        user_obj.password = encrypt(kwargs.get("password"))
        user_obj.user_role = ADMIN_USER if _is_first_user() else STANDARD_USER

        session.add(user_obj)
        session.flush()
        session.commit()
        app.logger.info("User Id :: {}".format(user_obj.id))

        return session.query(User).filter(User.id == user_obj.id).first().__dict__

    current_user = _add_user()
    return create_jwt_token(current_user)


def create_jwt_token(current_user):
    def _get_user_role_permission():
        permission_id = session.query(
            RolePermission.id
        ).filter(
            RolePermission.user_role_id == current_user.get("user_role"),
            RolePermission.is_deleted == ACTIVE
        )

        role_permission = session.query(
            Permission.name
        ).filter(
            Permission.id.in_(permission_id),
            Permission.is_deleted == ACTIVE
        ).all()

        permission_list = [permission.name for permission in role_permission]
        app.logger.debug("role permission :: {}".format(permission_list))
        return permission_list

    def _create_user_identity():
        return dict(
            user_id=current_user.get("id"),
            user_name=current_user.get("user_name"),
            email=current_user.get("email"),
            user_role=USER_ROLE.get(current_user.get("user_role"), STANDARD_USER),
            user_role_permission=_get_user_role_permission()
        )

    def _create_jwt_token():
        identity = _create_user_identity()
        identity = json.dumps(identity)
        return "Bearer {}".format(create_access_token(identity)), "Bearer {}".format(create_refresh_token(identity))

    return _create_jwt_token()
