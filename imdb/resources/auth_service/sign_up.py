from flask import current_app as app
from flask_restful import Resource, marshal_with, fields as field
from marshmallow import Schema, fields, validate
from webargs.flaskparser import use_kwargs

from imdb.functionality import sign_up
from utils import handle_exceptions


class SignUpRequest(Schema):
    user_name = fields.Str(required=True, allow_none=False)
    email = fields.Email(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=True)

    class Meta:
        strict = True


sign_up_response = dict(
    success=field.Boolean,
    message=field.String,
    data=dict(
        access_token=field.String,
        refresh_token=field.String
    )
)


class SignUp(Resource):
    method_decorators = [handle_exceptions]

    def __int__(self):
        app.logger.info("In constructor of {}".format(self.__class__.__name__))

    @use_kwargs(SignUpRequest)
    @marshal_with(sign_up_response)
    def post(self, **kwargs):
        access_token, refresh_token = sign_up(**kwargs)
        response = dict(
            success=True,
            message="User has been successfully created.!",
            access_token=access_token,
            refresh_token=refresh_token
        )
        app.logger.debug("Login Response :: {}".format(response))
        return response