import json
from functools import wraps

from flask import current_app as app
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from constant.common_constant import ACTIVE, USER_ROLE, STANDARD_USER
from model import session, User, Permission, RolePermission
from utils.common_utils import RolePermissionDeniedException


def authorize_request(role_permission, open_api=False):
    def wrapper(fn):
        @wraps(fn)
        def check_role_permission(*args, **kwargs):
            app.logger.info("Is API Open :: {}".format(open_api))

            def _get_identity_payload():
                app.logger.info("args :: {}, kwargs :: {}".format(args, kwargs))
                verify_jwt_in_request()
                return json.loads(get_jwt_identity())

            def _get_user():
                current_user_obj = session.query(
                    User
                ).filter(
                    User.id == identity_payload.get('user_id'),
                    User.is_deleted == ACTIVE
                ).first()

                return current_user_obj.__dict__ if current_user_obj else dict()

            def _get_user_role_permission(user_role_id):
                permission_id = session.query(
                    RolePermission.id
                ).filter(
                    RolePermission.user_role_id == user_role_id,
                    RolePermission.is_deleted == ACTIVE
                )

                user_permission = session.query(
                    Permission.name
                ).filter(
                    Permission.id.in_(permission_id),
                    Permission.is_deleted == ACTIVE
                ).all()

                return [permission[0] for permission in user_permission]

            def _prepare_identity():
                current_user = _get_user()
                return dict(
                    user_id=current_user.get("id"),
                    user_name=current_user.get("user_name"),
                    email=current_user.get("email"),
                    user_role=USER_ROLE.get(current_user.get("user_role"), STANDARD_USER),
                    user_role_permission=_get_user_role_permission(current_user.get("user_role"))
                )

            def _check_permission():
                app.logger.info("Role Permission :: {}".format(role_permission))
                if role_permission not in identity_payload['user_role_permission']:
                    raise RolePermissionDeniedException(
                        "User role has not access to this permission {}".format(role_permission)
                    )
                return None

            identity_payload = {}
            if not open_api:
                identity_payload = _get_identity_payload()
                # user_identity = _prepare_identity()
                app.logger.info("User Identity :: {}".format(identity_payload))
                _check_permission()
            return fn(identity_payload, *args, **kwargs)
        return check_role_permission
    return wrapper
