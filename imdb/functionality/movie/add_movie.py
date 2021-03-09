from flask import current_app as app

from model import Movie, session


def add_movie(current_user, **kwargs):
    app.logger.debug("Inside add_movie functionality.")

    def add_movie_obj():
        app.logger.info("Add movie request received by user :: {}".format(current_user.get("user_name")))
        movie_obj = Movie()
        movie_obj.name = kwargs.get("movie_name")
        movie_obj.popularity = kwargs.get("popularity")
        movie_obj.director = kwargs.get("director")
        movie_obj.genre = str(kwargs.get("genre"))
        movie_obj.imdb_score = kwargs.get("imdb_score")

        session.add(movie_obj)
        session.flush()
        session.commit()
        app.logger.info("New Movie Id :: {}".format(movie_obj.id))
        return movie_obj.id

    def _prepare_response():
        app.logger.debug("Preparing for response dict.")
        return dict(
                movie_id=movie_id,
                movie_name=kwargs.get("movie_name"),
                popularity=kwargs.get('popularity'),
                director=kwargs.get("director"),
                genre=kwargs.get("genre"),
                imdb_score=kwargs.get("imdb_score"),
            )

    movie_id = add_movie_obj()
    return _prepare_response()
