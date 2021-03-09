from flask import current_app as app
from flask_jwt_extended import jwt_required
from flask_restful import marshal_with, fields, Resource
from marshmallow import Schema, fields as field, validate
from webargs.flaskparser import use_kwargs

from imdb.functionality import update_movie
from utils import handle_exceptions, authorize_request
from constant.common_constant import IMDB_MOVIE_FULL_ACCESS


class UpdateMovieRequest(Schema):
    movie_id = field.Integer(required=True, allow_none=False)
    movie_name = field.Str(allow_none=False)
    popularity = field.Float(validate=[validate.Range(min=0, max=100)], allow_none=False)
    director = field.Str(allow_none=False)
    genre = field.List(field.Str, allow_none=False)
    imdb_score = field.Float(allow_none=False)

    class Meta:
        strict = True


update_movie_response = dict(
    success=fields.Boolean,
    message=fields.String,
    data=dict(
        movie_id=fields.Integer
    )
)


class UpdateMovie(Resource):
    method_decorators = [authorize_request(IMDB_MOVIE_FULL_ACCESS), handle_exceptions]

    def __init__(self):
        app.logger.info("Inside Constructor of {}".format(self.__class__.__repr__))

    @use_kwargs(UpdateMovieRequest)
    @marshal_with(update_movie_response)
    def post(self, user_identity, **kwargs):
        return update_movie(user_identity, **kwargs)
