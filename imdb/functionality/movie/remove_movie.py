from flask import current_app as app

from constant.common_constant import ACTIVE, DELETED
from model import session, Movie


def remove_movie(current_user, movie_id):
    app.logger.info("Request received for Delete Movie.")

    def _prepare_remove_movie():
        app.logger.info("Movie Id :: {}, User Id :: {}".format(movie_id, current_user.get("user_id")))
        movie = session.query(Movie).filter(
            Movie.id == movie_id,
            Movie.is_deleted == ACTIVE
        )

        movie_obj = movie.first()
        movie_obj = movie_obj.__dict__ if movie_obj else {}
        update_count = movie.update({"is_deleted": DELETED})
        app.logger.info("Update Count :: {}".format(update_count))

        if not update_count:
            raise ValueError("MOVIE-NOT-FOUND")
        return movie_obj

    def _prepare_response():
        movie_obj = _prepare_remove_movie()
        return dict(
            success=True,
            message="Movie has been successfully deleted.!!!",
            movie_id=movie_obj.get("id"),
            movie_name=movie_obj.get("name"),
            director=movie_obj.get("director"),
            genre=movie_obj.get("genre"),
            imdb_score=movie_obj.get("imdb_score")
        )

    return _prepare_response()
