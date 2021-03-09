from flask import current_app as app


from model import User, UserRole, Permission, RolePermission, session
from constant.common_constant import ACTIVE


def update_user_role(**kwargs):
    def _get_user_by_email():
        user_obj = session.query(User).filter(
            User.email == kwargs.get("email"),
            User.is_deleted == ACTIVE
        ).first()

        if not user_obj:
            raise ValueError("USER-NOT-FOUND")

        return user_obj

    def _get_user_role():
        user_role = session.query(UserRole).filter(
            UserRole.role_name == kwargs.get("user_role"),
            UserRole.is_deleted == ACTIVE
        ).first()

        if not user_role:
            raise ValueError("INVALID-USER-ROLE")

        return user_role

    def _update_user_role():
        update_count = session.query(User).filter(
            User.email == kwargs["email"],
            User.is_deleted == ACTIVE
        ).update({"user_role": user_role.id})

        app.logger.debug("Update User Role Count :: {}".format(update_count))
        return True

    def _get_user_role_permission():
        role_permission = session.query(Permission).filter(
            Permission.is_deleted == ACTIVE,
            Permission.id == RolePermission.permission_id,
            RolePermission.user_role_id == user_role.id,
            RolePermission.is_deleted == ACTIVE
        ).all()

        if not role_permission:
            return []

        return [permission.name for permission in role_permission]

    def _prepare_response():
        return dict(
            user_id=user.id,
            user_name=user.user_name,
            email=user.email,
            user_role=user_role.role_name,
            user_role_permission=_get_user_role_permission()
        )

    user = _get_user_by_email()
    user_role = _get_user_role()
    _update_user_role()
    return _prepare_response()
