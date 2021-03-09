import os
from datetime import timedelta


def os_env(key, default=None):
    try:
        return os.environ[key]
    except KeyError:
        if default is not None:
            return default

        raise Exception(
            "Environment-Variable '{}' "
            "is required and was not found".format(key))


SQLALCHEMY_DATABASE_URI = os_env("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = os_env("SQLALCHEMY_TRACK_MODIFICATIONS")
SQLALCHEMY_ECHO = os_env("SQLALCHEMY_ECHO")

DEFAULT_LOGGER_NAME = os_env('LOGGER_NAME')
FILE_LOG_CONFIG = {
    'log_level': os_env('LOG_LEVEL'),
    'absolute_log_file_path': os_env('LOGGER_FILE_PATH'),
    'formatter_string': '%(request_id)s - %(asctime)s - %(filename)s - %(module)s - %(funcName)s - '
                        '%(lineno)d - [%(levelname)s] - %(message)s',
    'kwargs': {
        'when': 'midnight',
        'backupCount': 0,
        'interval': 1,
        'utc': True
    }
}

# JWT Configurations
SECRET_KEY = 'QvBHYImKezV3h2XbH8y32HsC4yUHSUsM'
JWT_ACCESS_COOKIE_NAME = 'Authorization'
JWT_EXPIRATION_DELTA = timedelta(hours=48)
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=48)
JWT_COOKIE_CSRF_PROTECT = JWT_CSRF_IN_COOKIES = False
# JWT_AUTH_URL_RULE = ''
