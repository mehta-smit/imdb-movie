from functools import wraps

from flask import make_response, current_app as app
from marshmallow.exceptions import ValidationError, MarshmallowError
from werkzeug.exceptions import UnprocessableEntity, HTTPException, Unauthorized

from constant.common_constant import FAILED
from .common_utils import RolePermissionDeniedException
from model import session


__all__ = ["handle_exceptions", "handle_response"]


def handle_response(success, status_code, message, exception):
    response_dict = dict(
        success=success,
        message=message,
        data=dict(
            status_code=status_code,
            exception=exception
        )
    )
    app.logger.exception("Response :: {}".format(response_dict))
    response = make_response(response_dict)
    response.headers["Content-Type"] = "application/json"
    return response


def handle_exceptions(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        from model import close_session
        try:
            result = fn(*args, **kwargs)
        except RolePermissionDeniedException as exception:
            app.logger.error("This user is not allowed to access this API.")
            close_session(True)
            return handle_response(FAILED, 401, "INSUFFICIENT-ACCESS-PERMISSION", str(exception))
        except Unauthorized as exception:
            app.logger.error("Request Authorization Failed :: {}".format(exception))
            close_session(True)
            return handle_response(FAILED, 401, "Unauthorized Request", str(exception))
        except ValueError as val_err:
            app.logger.error(repr(val_err))
            close_session(True)
            return handle_response(FAILED, 500, "Payload Parsing Error", str(val_err))
        except (ValidationError, UnprocessableEntity) as val_err:
            app.logger.exception(repr(val_err))
            try:
                message = val_err.data.get("messages", None)
            except Exception as sa_err:
                message = sa_err.message
            close_session(True)
            return handle_response(FAILED, 400, "Request Failed", str(message))
        except MarshmallowError as exc:
            app.logger.exception(exc)
            close_session(True)
            return handle_response(FAILED, 400, "Payload Validation Failed", str(exc))
        except HTTPException as exc:
            app.logger.exception(exc)
            close_session(True)
            return handle_response(FAILED, 400, "Request Failed", str(exc))
        except (Exception, KeyError, AttributeError) as exc:
            app.logger.exception(exc)
            close_session(True)
            return handle_response(FAILED, 500, "Internal Server Error", str(exc))
        else:
            session.commit()
            return result

    return wrapper
