from flask import current_app as app
from flask_restful import Resource, marshal_with, fields as field

from constant.common_constant import IMDB_USER_ROLE_FULL_ACCESS
from imdb.functionality import list_user_role
from utils import authorize_request, handle_exceptions

list_user_role_response = dict(
    success=field.Boolean,
    message=field.String,
    data=dict(
        user_role=field.Nested(dict(
            role_id=field.Integer,
            role_name=field.String,
            role_permission=field.List(field.String)
        ))
    )
)


class ListUserRole(Resource):
    method_decorators = [authorize_request(IMDB_USER_ROLE_FULL_ACCESS), handle_exceptions]

    def __int__(self):
        app.logger.info("In constructor of {}".format(self.__class__.__name__))

    @marshal_with(list_user_role_response)
    def get(self, user_identity, **kwargs):
        app.logger.debug("A request for list of user role received.")
        user_role_data = list_user_role()

        return dict(
            success=True,
            message="List of user role",
            user_role=user_role_data
        )
