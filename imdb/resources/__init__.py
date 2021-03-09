from flask_restful import Api

from .movie import AddMovie, UpdateMovie, RemoveMovie, ListMovie
from .auth_service import SignUp, Login
from .user import ListUser, ListUserRole, UpdateUserRole


def init_api(app):
    api = Api(app, prefix='/imdb')

    _register_api(api)


def _register_api(api):
    # IMDB Movie APIs
    api.add_resource(AddMovie, '/movie/add')  # Adds Movie
    api.add_resource(UpdateMovie, '/movie/update')  # Updates Movie
    api.add_resource(RemoveMovie, '/movie/remove')  # Remove Movie
    api.add_resource(ListMovie, '/movie/list')  # List Movie

    # User API
    api.add_resource(ListUser, '/user/list')
    api.add_resource(UpdateUserRole, '/user/role/update')
    api.add_resource(ListUserRole, '/role/list')

    # Authorization API
    api.add_resource(SignUp, '/signUp')  # SignUp API
    api.add_resource(Login, '/signIn')  # SignIn API
