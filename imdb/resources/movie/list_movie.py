from flask import current_app as app
from flask_jwt_extended import jwt_required
from flask_restful import Resource, fields, marshal_with
from marshmallow import fields as field, Schema
from webargs.flaskparser import use_kwargs

from constant.common_constant import IMDB_MOVIE_VIEW
from imdb.functionality import list_movie
from utils import handle_exceptions, authorize_request


class ListMovieRequest(Schema):
    movie_name = field.Str(allow_none=False)
    popularity = field.Float(allow_none=False)
    director = field.Str(allow_none=False)
    genre = field.Str(allow_none=False)
    imdb_score = field.Float(allow_none=False)
    offset = field.Integer(required=False, allow_none=False, default=1)
    count = field.Integer(allow_none=False, default=10)

    class Meta:
        strict = True


list_movie_response = dict(
    success=fields.Boolean,
    message=fields.String,
    data=dict(
        total_count=fields.Integer,
        movies=fields.Nested(
            dict(
                movie_id=fields.Integer,
                movie_name=fields.String,
                popularity=fields.Float,
                director=fields.String,
                genre=fields.String,
                imdb_score=fields.Float
            )
        )
    )
)


class ListMovie(Resource):
    method_decorators = [jwt_required(optional=True), authorize_request(IMDB_MOVIE_VIEW, open_api=True), handle_exceptions]

    def __int__(self):
        app.logger.info("Inside constructor of {}".format(self.__class__.__name__))

    @use_kwargs(ListMovieRequest)
    @marshal_with(list_movie_response)
    def post(self, current_uer, **kwargs):
        app.logger.info(kwargs)
        return list_movie(current_uer, **kwargs)
