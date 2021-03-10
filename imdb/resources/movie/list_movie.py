from flask import current_app as app
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from marshmallow import fields, Schema, validate

from constant.common_constant import IMDB_MOVIE_VIEW
from imdb.functionality import list_movie
from utils import handle_exceptions, authorize_request


class ListMovieRequest(Schema):
    movie_name = fields.Str(allow_none=False)
    popularity = fields.Float(required=False, validate=[validate.Range(min=0, max=100)], allow_none=False)
    director = fields.Str(allow_none=False)
    genre = fields.List(fields.Str, allow_none=False)
    imdb_score = fields.Float(required=False, allow_none=False, validate=[validate.Range(min=0, max=10)])
    offset = fields.Integer(required=False, allow_none=False, default=1)
    count = fields.Integer(allow_none=False, default=10)

    class Meta:
        strict = True


class NestedMoviesResponse(Schema):
    movies = fields.Dict(
        movie_id=fields.Integer(),
        movie_name=fields.Str(),
        popularity=fields.Float(),
        director=fields.Str(),
        genre=fields.Str(),
        imdb_score=fields.Float()
    )


class ListMovieResponse(Schema):
    success = fields.Boolean()
    message = fields.Str()
    data = fields.Dict(
        total_count=fields.Integer(),
        movies=fields.Nested(NestedMoviesResponse)
    )


class ListMovie(MethodResource, Resource):
    method_decorators = [jwt_required(optional=True), authorize_request(IMDB_MOVIE_VIEW, open_api=True),
                         handle_exceptions]

    def __int__(self):
        app.logger.info("Inside constructor of {}".format(self.__class__.__name__))

    @doc(tags=["List Movie"], description="An API for List IMDB Movie.")
    @use_kwargs(ListMovieRequest)
    @marshal_with(ListMovieResponse)
    def post(self, current_uer, **kwargs):
        app.logger.info(kwargs)
        return list_movie(current_uer, **kwargs)
