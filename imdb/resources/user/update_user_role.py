from flask import current_app as app
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource
from marshmallow import Schema, fields

from constant.common_constant import IMDB_USER_FULL_ACCESS
from imdb.functionality import update_user_role
from utils import authorize_request, handle_exceptions


class UpdateUserRoleRequest(Schema):
    user_role = fields.String(required=True, allow_none=False)
    email = fields.Email(required=True, allow_none=False)

    class Meta:
        strict = True


class UpdateUserRoleRespone(Schema):
    success = fields.Boolean()
    message = fields.Str()
    data = fields.Dict(
        user_id=fields.Integer(),
        user_name=fields.Str(),
        email=fields.Str(),
        user_role=fields.Str(),
        user_role_permission=fields.List(fields.Str())
    )


class UpdateUserRole(MethodResource, Resource):
    method_decorators = [authorize_request(IMDB_USER_FULL_ACCESS), handle_exceptions]

    def __init__(self):
        app.logger.info("In constructor of {}".format(self.__class__.__name__))

    @doc(tags=["Update User Role"], description="An API to update user role and modify it's permission.")
    @use_kwargs(UpdateUserRoleRequest)
    @marshal_with(UpdateUserRoleRespone)
    def post(self, user_identity, **kwargs):
        app.logger.debug(
            "A request to update user role is received by the user :: {}".format(user_identity["user_name"]))
        app.logger.info("In post request of update user role with kwargs {}".format(kwargs))
        response = update_user_role(**kwargs)

        return dict(
            success=True,
            message="User role has been successfully updated.!!!",
            data=response
        )
