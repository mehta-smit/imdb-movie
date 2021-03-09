from flask import current_app as app
from flask_restful import Resource, fields as field, marshal_with
from marshmallow import Schema, fields
from webargs.flaskparser import use_kwargs

from imdb.functionality import login
from utils import handle_exceptions


class LoginRequest(Schema):
    email = fields.Email(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=False)

    class Meta:
        strict = True


login_response = dict(
    success=field.Boolean,
    message=field.String,
    data=dict(
        access_token=field.String,
        refresh_token=field.String
    )
)


class Login(Resource):
    method_decorators = [handle_exceptions]

    def __init__(self):
        app.logger.info("In Constructor of {}".format(self.__class__.__name__))

    @use_kwargs(LoginRequest)
    @marshal_with(login_response)
    def post(self, **kwargs):
        access_token, refresh_token = login(**kwargs)
        response = dict(
            success=True,
            message="Successfully logged in.!!!",
            access_token=access_token,
            refresh_token=refresh_token

        )
        app.logger.debug("Login Response :: {}".format(response))
        return response
