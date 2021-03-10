import json

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_apispec.extension import FlaskApiSpec
from flask_cors import CORS
from flask_jwt import JWT
from flask_jwt_extended import JWTManager

from constant.common_constant import FLASK_APP_NAME, FLASK_CONFIG_MODULE
from model.base import db, migrate
from utils.logger import config_logger
from .resources import init_api


def create_flask_app():
    """
        Create flask app, configure the app, configure database session
        :returns: instance of flask
    """

    def _make_app():
        app = Flask(FLASK_APP_NAME)
        app.config.from_object(FLASK_CONFIG_MODULE)

        with app.app_context():
            app.config.update({
                'APISPEC_SPEC': APISpec(
                    title='IMDB Movie',
                    version='v1',
                    plugins=[MarshmallowPlugin()],
                    openapi_version='2.0.0'
                ),
                'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
                'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
            })
            docs = FlaskApiSpec(app)

            config_logger(app)
            create_restful_api(app, docs)

            db.init_app(app)
            migrate.init_app(app, db)
        return app

    def teardown_app():
        from model import close_session
        flask_app.teardown_request(close_session)
        flask_app.teardown_appcontext(close_session)

    def _enable_jwt_auth():
        def authenticate():
            return True

        def load_user(payload):
            identity_payload = json.loads(payload['identity'])
            identity = identity_payload['user_id']
            return identity

        jwt = JWT(flask_app, authenticate, load_user)
        JWTManager(flask_app)
        return jwt

    flask_app = _make_app()
    _enable_jwt_auth()
    teardown_app()
    return flask_app


def create_restful_api(app, docs):
    # added cors as it was only giving pre-flight request
    # CORS(app, resources={r"/*": {"origins": "*"}})
    init_api(app, docs)
