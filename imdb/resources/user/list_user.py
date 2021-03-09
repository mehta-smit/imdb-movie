from flask import current_app as app
from flask_restful import Resource, marshal_with, fields as field
from marshmallow import Schema, fields
from webargs.flaskparser import use_kwargs

from constant.common_constant import IMDB_USER_FULL_ACCESS
from imdb.functionality import list_user
from utils import handle_exceptions, authorize_request


class ListUserRequest(Schema):
    user_name = fields.Str(required=False, allow_none=False)
    email = fields.Str(required=False, allow_none=False)

    class Meta:
        strict = True


list_user_response = dict(
    success=field.Boolean,
    message=field.String,
    data=dict(
        users=field.Nested(dict(
                user_id=field.Integer,
                user_name=field.String,
                email=field.String,
                user_role=field.String,
                create_at=field.DateTime,
                is_active=field.Boolean
            ))
    )
)


class ListUser(Resource):
    method_decorators = [handle_exceptions, authorize_request(IMDB_USER_FULL_ACCESS)]

    def __init__(self):
        app.logger.info("Inside constructor of {}".format(self.__class__.__name__))

    @use_kwargs(ListUserRequest)
    @marshal_with(list_user_response)
    def get(self, current_user, **kwargs):
        user_data = list_user(current_user, **kwargs)
        app.logger.debug("List User Response :: {}".format(user_data))

        return dict(
            success=True,
            message="List of Users.",
            users=user_data

        )
