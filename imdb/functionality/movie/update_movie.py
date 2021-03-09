from flask import current_app as app

from model import Movie, session
from constant.common_constant import ACTIVE


def update_movie(current_user, **kwargs):
    app.logger.debug("Inside update_movie functionality.")
    movie_id = kwargs.pop("movie_id")

    def _prepare_update_movie():
        app.logger.info("Movie ID :: {}, user :: {}".format(
            movie_id, current_user.get("user_name")
        ))

        update_dict = dict()
        if 'movie_name' in kwargs.keys():
            update_dict["name"] = kwargs.pop("movie_name")

        if 'genre' in kwargs.keys():
            update_dict['genre'] = str(kwargs.pop("genre"))

        update_dict.update(kwargs)

        update_count = session.query(Movie).filter(
            Movie.id == movie_id,
            Movie.is_deleted == ACTIVE
        ).update(update_dict)

        app.logger.info("Update Count :: {}".format(update_count))

    def _prepare_response():
        app.logger.debug("Preparing for response dict.")
        return dict(
            success=True,
            message="Movie has been successfully updated.!!!",
            data=dict(
                movie_id=movie_id
            )
        )

    _prepare_update_movie()
    return _prepare_response()
