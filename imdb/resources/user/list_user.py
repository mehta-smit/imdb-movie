from flask import current_app as app
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource
from marshmallow import Schema, fields

from constant.common_constant import IMDB_USER_FULL_ACCESS
from imdb.functionality import list_user
from utils import handle_exceptions, authorize_request


class ListUserRequest(Schema):
    user_name = fields.String(required=False, allow_none=False)
    email = fields.String(required=False, allow_none=False)

    class Meta:
        strict = True


class NestedUserList(Schema):
    users = fields.Dict(
        user_id=fields.Integer(),
        user_name=fields.Str(),
        email=fields.Str(),
        user_role=fields.Str(),
        created_at=fields.DateTime(),
        is_active=fields.Boolean()
    )


class ListUserResponse(Schema):
    success = fields.Boolean()
    message = fields.Str()
    data = fields.Dict(
        users=fields.Nested(NestedUserList)
    )


class ListUser(MethodResource, Resource):
    method_decorators = [handle_exceptions, authorize_request(IMDB_USER_FULL_ACCESS)]

    def __init__(self):
        app.logger.info("Inside constructor of {}".format(self.__class__.__name__))

    @doc(tags=["List User"], description="An API to list all users and filter user as well.")
    @use_kwargs(ListUserRequest)
    @marshal_with(ListUserResponse)
    def get(self, current_user, **kwargs):
        app.logger.debug("Kwargs :: {}".format(kwargs))
        user_data = list_user(current_user, **kwargs)
        app.logger.debug("List User Response :: {}".format(user_data))

        return dict(
            success=True,
            message="List of Users.",
            data=dict(users=user_data)
        )
