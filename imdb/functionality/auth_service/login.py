from flask import current_app as app

from model import User, session
from constant.common_constant import ACTIVE, PASSWORD_ATTEMPT
from utils.common_utils import decrypt
from .sign_up import create_jwt_token


def login(**kwargs):
    def _get_user():
        user_obj = session.query(User).filter(
            User.email == kwargs["email"],
            User.is_deleted == ACTIVE
        ).first()

        if not user_obj:
            raise Exception("USER-NOT-FOUND")

        if user_obj.pwd_attempt >= PASSWORD_ATTEMPT:
            raise Exception("USER-BLOCKED-DUE-TO-MAXIMUM-RETRY-EXCEEDS")
        return user_obj

    def _verify_user():
        decrypted_pwd = decrypt(user.password)

        if kwargs['password'] != decrypted_pwd:
            session.query(User).filter(
                User.email == user.email,
                User.is_deleted == ACTIVE
            ).update(**{"pwd_attempt": user.pwd_attempt + 1})
            session.commit()

            raise Exception("WRONG-PASSWORD")
        return True

    user = _get_user()
    if _verify_user():
        return create_jwt_token(user.__dict__)
