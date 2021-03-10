from flask import current_app as app
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from flask_restful import Resource
from marshmallow import Schema, fields

from constant.common_constant import IMDB_USER_ROLE_FULL_ACCESS
from imdb.functionality import list_user_role
from utils import authorize_request, handle_exceptions


class ListUserRoleResponse(Schema):
    success = fields.Boolean()
    message = fields.Str()
    data = fields.Dict(
        user_role=fields.Dict(
            role_id=fields.Integer,
            role_name=fields.String,
            role_permission=fields.List(fields.Str())
        )
    )


class ListUserRole(MethodResource, Resource):
    method_decorators = [authorize_request(IMDB_USER_ROLE_FULL_ACCESS), handle_exceptions]

    def __int__(self):
        app.logger.info("In constructor of {}".format(self.__class__.__name__))

    @doc(tags=["List User Role"], description="An API to List User Role.")
    @marshal_with(ListUserRoleResponse)
    def get(self, user_identity, **kwargs):
        app.logger.debug("A request for list of user role received.")
        user_role_data = list_user_role()

        return dict(
            success=True,
            message="List of user role",
            data=dict(user_role=user_role_data)
        )
