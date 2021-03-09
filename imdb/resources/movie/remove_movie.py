from flask import current_app as app
from flask_jwt_extended import jwt_required
from flask_restful import Resource, fields, marshal_with
from marshmallow import fields as field, Schema
from webargs.flaskparser import use_kwargs

from imdb.functionality import remove_movie
from utils import handle_exceptions, authorize_request
from constant.common_constant import IMDB_MOVIE_FULL_ACCESS


class RemoveMovieRequest(Schema):
    movie_id = field.Integer(required=True, allow_none=False)

    class Meta:
        strict = True


remove_movie_response = dict(
    success=fields.Boolean,
    message=fields.String,
    data=dict(
        movie_id=fields.Integer,
        movie_name=fields.String,
        popularity=fields.Float,
        director=fields.String,
        genre=fields.String,
        imdb_score=fields.Float
    )
)


class RemoveMovie(Resource):
    method_decorators = [authorize_request(IMDB_MOVIE_FULL_ACCESS), handle_exceptions]

    def __int__(self):
        app.logger.debug("In constructor of {}".format(self.__class__.__repr__))

    @use_kwargs(RemoveMovieRequest)
    @marshal_with(remove_movie_response)
    def delete(self, current_user, **kwargs):
        return remove_movie(current_user, kwargs["movie_id"])
