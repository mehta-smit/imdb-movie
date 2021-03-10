from flask import current_app as app
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource
from marshmallow import Schema, fields, validate

from constant.common_constant import IMDB_MOVIE_FULL_ACCESS
from imdb.functionality import add_movie
from utils import handle_exceptions, authorize_request


class AddMovieRequest(Schema):
    movie_name = fields.Str(required=True, allow_none=False)
    popularity = fields.Float(required=True, validate=[validate.Range(min=0, max=100)], allow_none=False)
    director = fields.Str(required=True, allow_none=False)
    genre = fields.List(fields.Str, allow_none=False)
    imdb_score = fields.Float(required=True, allow_none=False, validate=[validate.Range(min=0, max=10)])

    class Meta:
        strict = True


class AddMovieResponse(Schema):
    success = fields.Boolean()
    message = fields.Str()
    data = fields.Dict(
        movie_id=fields.Integer(),
        movie_name=fields.Str(),
        property=fields.Float(),
        director=fields.Str(),
        genre=fields.Str(),
        imdb_score=fields.Float()
    )


class AddMovie(MethodResource, Resource):
    method_decorators = [authorize_request(IMDB_MOVIE_FULL_ACCESS), handle_exceptions]

    def __init__(self):
        app.logger.info("Inside Constructor of {}".format(self.__class__.__name__))

    @doc(tags=["Add Movie"], description="Adds a movie in IMDB.")
    @use_kwargs(AddMovieRequest)
    @marshal_with(AddMovieResponse)
    def post(self, user_identity, **kwargs):
        app.logger.debug("Inside Add Movie Post Request.")
        response = add_movie(user_identity, **kwargs)
        app.logger.info("Add Movie Response :: {}".format(response))
        return dict(
            success=True,
            message="Movie has been successfully added.!",
            data=response
        )
