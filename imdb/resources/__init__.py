from flask_restful import Api

from .movie import AddMovie, UpdateMovie, RemoveMovie, ListMovie
from .auth_service import SignUp, Login
from .user import ListUser, ListUserRole, UpdateUserRole


def init_api(app, docs):
    api = Api(app, prefix='/imdb')

    _register_api(api, docs)


def _register_api(api, docs):
    # IMDB Movie APIs
    api.add_resource(AddMovie, '/movie/add')  # Adds Movie
    docs.register(AddMovie)

    api.add_resource(UpdateMovie, '/movie/update')  # Updates Movie
    docs.register(UpdateMovie)

    api.add_resource(RemoveMovie, '/movie/remove')  # Remove Movie
    docs.register(RemoveMovie)

    api.add_resource(ListMovie, '/movie/list')  # List Movie
    docs.register(ListMovie)

    # User API
    api.add_resource(ListUser, '/user/list')
    docs.register(ListUser)

    api.add_resource(UpdateUserRole, '/user/role/update')
    docs.register(UpdateUserRole)

    api.add_resource(ListUserRole, '/role/list')
    docs.register(ListUserRole)

    # Authorization API
    api.add_resource(SignUp, '/signUp')  # SignUp API
    docs.register(SignUp)

    api.add_resource(Login, '/signIn')  # SignIn API
    docs.register(Login)
