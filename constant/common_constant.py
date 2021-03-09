# This module is used for having all common constants
# Used by our flask application.

FLASK_APP_NAME = "imdb-movie"
FLASK_CONFIG_MODULE = "config"

ACTIVE, DELETED = 0, 1
ADMIN_USER, STANDARD_USER = 1, 2
USER_ROLE = {
    ADMIN_USER: "admin", STANDARD_USER: "standard"
}

PASSWORD_ATTEMPT = 3
SUCCESS, FAILED = True, False

IMDB_MOVIE_FULL_ACCESS = "imdb_movie_full_access"
IMDB_MOVIE_VIEW = "imdb_movie_view"
IMDB_USER_FULL_ACCESS = "imdb_user_full_access"
IMDB_USER_ROLE_FULL_ACCESS = "imdb_user_role_full_access"
IMDB_USER_CREATE = "imdb_user_create"
IMDB_USER_VIEW = "imdb_user_view"
