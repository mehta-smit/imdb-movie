from flask import current_app as app

from constant.common_constant import PASSWORD_ATTEMPT, ACTIVE
from model import User, session, UserRole


def list_user(current_user, **kwargs):
    app.logger.info("Request for list user received by user {}".format(current_user.get("user_name")))

    def _get_user():
        input_keys = kwargs.keys()
        query = session.query(User)
        if 'user_name' in input_keys:
            query = query.filter(User.user_name.like("%{}%".format(kwargs['user_name'])))

        if 'email' in input_keys:
            query = query.filter(User.email == kwargs['email'])

        query = query.filter(UserRole.id == User.user_role)
        query.order_by(User.id.desc())

        app.logger.info("List User Query :: {}".format(query))
        users = query.all()
        if not users:
            return []
        return users

    def _get_user_role(user_role):
        user_role = session.query(UserRole).filter(
            UserRole.id == user_role,
            UserRole.is_deleted == ACTIVE
        ).first()

        if not user_role:
            raise ValueError("USER-ROLE-NOT-FOUND")
        return user_role

    def _prepare_response():
        user_data = list()

        for user in _get_user():
            user_role = _get_user_role(user.user_role)
            user_data.append(dict(
                user_id=user.id,
                user_name=user.user_name,
                email=user.email,
                user_role=user_role.role_name,
                create_at=user.created_at,
                is_active=False if user.pwd_attempt >= PASSWORD_ATTEMPT else True
            ))

        return user_data

    return _prepare_response()
