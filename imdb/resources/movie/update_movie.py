from flask import current_app as app
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource
from marshmallow import Schema, fields, validate

from constant.common_constant import IMDB_MOVIE_FULL_ACCESS
from imdb.functionality import update_movie
from utils import handle_exceptions, authorize_request


class UpdateMovieRequest(Schema):
    movie_id = fields.Integer(required=True, allow_none=False)
    movie_name = fields.Str(allow_none=False)
    popularity = fields.Float(validate=[validate.Range(min=0, max=100)], allow_none=False)
    director = fields.Str(allow_none=False)
    genre = fields.List(fields.Str, allow_none=False)
    imdb_score = fields.Float(allow_none=False, validate=[validate.Range(min=0, max=10)])

    class Meta:
        strict = True


class UpdateMovieResponse(Schema):
    success = fields.Boolean()
    message = fields.Str(),
    data = fields.Dict(
        movie_id=fields.Integer()
    )


class UpdateMovie(MethodResource, Resource):
    method_decorators = [authorize_request(IMDB_MOVIE_FULL_ACCESS), handle_exceptions]

    def __init__(self):
        app.logger.info("Inside Constructor of {}".format(self.__class__.__repr__))

    @doc(tags=["Update Movie"], description="An API to update movie in IMDB.")
    @use_kwargs(UpdateMovieRequest)
    @marshal_with(UpdateMovieResponse)
    def post(self, user_identity, **kwargs):
        return update_movie(user_identity, **kwargs)
