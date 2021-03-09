from flask import current_app as app
from flask_restful import Resource, marshal_with, fields as field
from marshmallow import Schema, fields
from webargs.flaskparser import use_kwargs

from imdb.functionality import update_user_role
from constant.common_constant import IMDB_USER_FULL_ACCESS
from utils import authorize_request, handle_exceptions


class UpdateUserRoleRequest(Schema):
    user_role = fields.String(required=True, allow_none=False)
    email = fields.Email(required=True, allow_none=False)

    class Meta:
        strict = True


update_user_role_response = dict(
    success=field.Boolean,
    message=field.String,
    data=dict(
        user_id=field.Integer,
        user_name=field.String,
        email=field.String,
        user_role=field.String,
        user_role_permission=field.List(field.String)
    )
)


class UpdateUserRole(Resource):
    method_decorators = [authorize_request(IMDB_USER_FULL_ACCESS), handle_exceptions]

    def __init__(self):
        app.logger.info("In constructor of {}".format(self.__class__.__name__))

    @use_kwargs(UpdateUserRoleRequest)
    @marshal_with(update_user_role_response)
    def post(self, user_identity, **kwargs):
        app.logger.debug("A request to update user role is received by the user :: {}".format(user_identity["user_name"]))
        app.logger.info("In post request of update user role with kwargs {}".format(kwargs))
        response = update_user_role(**kwargs)

        return dict(
            success=True,
            message="User role has been successfully updated.!!!",
            **response
        )
