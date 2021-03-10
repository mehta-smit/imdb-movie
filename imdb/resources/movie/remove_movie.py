from flask import current_app as app
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource
from marshmallow import Schema, fields

from constant.common_constant import IMDB_MOVIE_FULL_ACCESS
from imdb.functionality import remove_movie
from utils import handle_exceptions, authorize_request


class RemoveMovieRequest(Schema):
    movie_id = fields.Integer(required=True, allow_none=False)

    class Meta:
        strict = True


class RemoveMovieResponse(Schema):
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


class RemoveMovie(MethodResource, Resource):
    method_decorators = [authorize_request(IMDB_MOVIE_FULL_ACCESS), handle_exceptions]

    def __int__(self):
        app.logger.debug("In constructor of {}".format(self.__class__.__repr__))

    @doc(tags=["Remove Movie"], description="An API to remove movie from IMDB.")
    @use_kwargs(RemoveMovieRequest)
    @marshal_with(RemoveMovieResponse)
    def delete(self, current_user, **kwargs):
        return remove_movie(current_user, kwargs["movie_id"])
