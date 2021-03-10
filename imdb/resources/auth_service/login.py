from flask import current_app as app
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource, fields as field
from marshmallow import Schema, fields

from imdb.functionality import login
from utils import handle_exceptions


class LoginRequest(Schema):
    email = fields.Email(required=True, allow_none=False)
    password = fields.String(required=True, allow_none=False)

    class Meta:
        strict = True


class LoginResponse(Schema):
    success = fields.Boolean()
    message = fields.Str()
    data = fields.Dict(
        access_token=fields.Str(),
        refresh_tokem=fields.Str()
    )


class Login(MethodResource, Resource):
    method_decorators = [handle_exceptions]

    def __init__(self):
        app.logger.info("In Constructor of {}".format(self.__class__.__name__))

    @doc(tags=["IMDB SignIn"], description="An SignIn IMDB API.")
    @use_kwargs(LoginRequest)
    @marshal_with(LoginResponse)
    def post(self, **kwargs):
        access_token, refresh_token = login(**kwargs)
        response = dict(
            success=True,
            message="Successfully logged in.!!!",
            data=dict(
                access_token=access_token,
                refresh_token=refresh_token
            )
        )
        app.logger.debug("Login Response :: {}".format(response))
        return response
