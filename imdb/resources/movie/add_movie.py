from flask import current_app as app
from flask_jwt_extended import jwt_required
from flask_restful import marshal_with, fields, Resource
from marshmallow import Schema, fields as field, validate
from webargs.flaskparser import use_kwargs

from constant.common_constant import IMDB_MOVIE_FULL_ACCESS
from imdb.functionality import add_movie
from utils import handle_exceptions, authorize_request


class AddMovieRequest(Schema):
    movie_name = field.Str(required=True, allow_none=False)
    popularity = field.Float(required=True, validate=[validate.Range(min=0, max=100)], allow_none=False)
    director = field.Str(required=True, allow_none=False)
    genre = field.Str(required=True, allow_none=False)
    imdb_score = field.Float(required=True, allow_none=False)

    class Meta:
        strict = True


add_movie_response = dict(
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


class AddMovie(Resource):
    method_decorators = [authorize_request(IMDB_MOVIE_FULL_ACCESS), handle_exceptions]

    def __init__(self):
        app.logger.info("Inside Constructor of {}".format(self.__class__.__name__))

    @use_kwargs(AddMovieRequest)
    @marshal_with(add_movie_response)
    def post(self, user_identity, **kwargs):
        app.logger.debug("Inside Add Movie Post Request.")
        response = add_movie(user_identity, **kwargs)
        app.logger.info("Add Movie Response :: {}".format(response))
        return dict(
            success=True,
            message="Movie has been successfully added.!",
            **response
        )
