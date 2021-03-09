"""
   Basic utilities used throughout the project
"""

import logging.config
from logging import Formatter
from logging.handlers import WatchedFileHandler
from uuid import uuid4

import flask

__author__ = "Smit R. Mehta"
__author_email__ = "mehtasmit44@gmail.com"
__description__ = "Logger module will be used to configure logger for our application."


def config_logger(app):
    file_log_config = app.config['FILE_LOG_CONFIG']
    log_file_path = file_log_config['absolute_log_file_path']
    handler = WatchedFileHandler(log_file_path)
    handler.setFormatter(Formatter(file_log_config['formatter_string']))

    logging_filter = logging.Filter()
    logging_filter.filter = RequestIdFilter().filter
    app.logger.addFilter(logging_filter)
    app.logger.addHandler(handler)

    app.logger.propagate = False
    app.logger.setLevel(file_log_config['log_level'])
    app.logger.debug("Logger Configured.!")


class Singleton(type):
    """
    This class is a metaclass of Logger class. It make it singleton.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


def generate_request_id(original_id=None):
    """
    Generate a new request ID, optionally including an original request ID
    """
    return original_id if original_id else str(uuid4())


class RequestId(object):
    __metaclass__ = Singleton

    def __init__(self, log_id='', original_log_id=''):
        self.log_id = log_id
        self.original_log_id = original_log_id
        self.set_log_id(self.log_id)

    def set_log_id(self, log_id):
        if not log_id and flask.has_request_context():
            self.log_id = getattr(flask.g, 'request_id', None)

    def generate_request_id(self, original_id=''):
        """
        Generate a new request ID, optionally including an original request ID
        """
        return original_id if original_id else str(uuid4())

    def request_id(self):
        """
        Returns the current request ID or a new one if there is none
        In order of preference:
            * If we've already created a request ID and stored it in the flask.g context local, use that
            * If a client has passed in the X-Request-Id header, create a new ID with that prepended
            * Otherwise, generate a request ID and store it in flask.g.request_id
        """
        if flask.has_request_context():
            if self.log_id and getattr(flask.g, 'request_id', None) == self.log_id:
                return self.log_id

            headers = flask.request.headers
            original_log_id = headers.get("X-Request-Id") or headers.get('HTTP_X_REQUEST_ID')
            self.log_id = flask.g.request_id = self.generate_request_id(original_log_id)

        if not self.log_id:
            new_uuid = self.generate_request_id()
            self.log_id = new_uuid

        return self.log_id


class RequestIdFilter(logging.Filter):
    """
    This is a logging filter that makes the request ID available for use in
    the logging format. Note that we're checking if we're in a request
    context, as we may want to log things before Flask is fully loaded.
    """

    def filter(self, record):
        request_id = RequestId().request_id()

        if flask.has_request_context():
            record.request_id = request_id
        else:
            record.request_id = request_id
        return True