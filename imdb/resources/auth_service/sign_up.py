from flask import current_app as app
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource
from marshmallow import Schema, fields

from imdb.functionality import sign_up
from utils import handle_exceptions


class SignUpRequest(Schema):
    user_name = fields.Str(required=True, allow_none=False)
    email = fields.Email(required=True, allow_none=False)
    password = fields.Str(required=True, allow_none=True)

    class Meta:
        strict = True


class SingUpResponse(Schema):
    success = fields.Boolean()
    message = fields.Str()
    data = fields.Dict(
        access_token=fields.Str(),
        refresh_tokem=fields.Str()
    )


class SignUp(MethodResource, Resource):
    method_decorators = [handle_exceptions]

    def __int__(self):
        app.logger.info("In constructor of {}".format(self.__class__.__name__))

    @doc(tags=["IMDB SignUp"], decription="An IMDB SignUp API.")
    @use_kwargs(SignUpRequest)
    @marshal_with(SingUpResponse)
    def post(self, **kwargs):
        access_token, refresh_token = sign_up(**kwargs)
        response = dict(
            success=True,
            message="User has been successfully created.!",
            data=dict(
                access_token=access_token,
                refresh_token=refresh_token
            )
        )
        app.logger.debug("Login Response :: {}".format(response))
        return response
