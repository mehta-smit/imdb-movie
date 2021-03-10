import operator

from flask import current_app as app

from model import Movie, session
from constant.common_constant import ACTIVE


def list_movie(current_user, **kwargs):
    app.logger.info("List movie request received by user {}".format(current_user.get("user_name")))

    def _prepare_dynamic_filter():
        query = session.query(Movie)

        if 'movie_name' in kwargs:
            query = query.filter(Movie.name.like("%{}%".format(kwargs['movie_name'])))

        if 'popularity' in kwargs:
            query = query.filter(Movie.popularity >= kwargs['popularity'])

        if 'director' in kwargs:
            query = query.filter(Movie.director.like("%{}%".format(kwargs['director'])))

        if 'genre' in kwargs:
            query = query.filter(Movie.genre.like("%{}%".format(kwargs['genre'])))

        if 'imdb_score' in kwargs:
            query = query.filter(Movie.imdb_score >= kwargs['imdb_score'])

        query.filter(Movie.is_deleted == ACTIVE)
        return query

    def _get_data():
        query = _prepare_dynamic_filter()
        total_count = query.count()
        limit = kwargs.get("count", 10)
        offset = kwargs.get("offset", 0)

        query.order_by(Movie.id.desc())
        app.logger.info("Total Nos, of records :: {}".format(total_count))

        if total_count > limit:
            query = query.offset(offset*limit).limit(limit)

        data = query.all()
        return _convert_objects_into_response(total_count, data)

    def _convert_objects_into_response(total_count, data):
        response = dict(
            success=True,
            message="Success.!!!",
            data=dict(
                total_count=total_count,
                movies=list(dict(
                    movie_id=movie.id,
                    movie_name=movie.name,
                    director=movie.director,
                    genre=movie.genre,
                    popularity=movie.popularity,
                    imdb_score=movie.imdb_score
                ) for movie in data)
            )
        )
        # app.logger.info("List Movie Response :: {}".format(response))
        return response

    return _get_data()
