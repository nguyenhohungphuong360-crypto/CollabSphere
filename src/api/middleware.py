import logging
from functools import wraps
from flask import request, g, current_app, jsonify
from marshmallow import ValidationError
from domain.exceptions import CustomException
from api.responses import error_response, unauthorized_response
import jwt

logger = logging.getLogger(__name__)


def token_required(f):
    """Decorator to protect routes requiring JWT authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return unauthorized_response("Authorization token is missing")

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return unauthorized_response("Invalid Authorization header format. Expected 'Bearer <token>'")

        token = parts[1]
        secret = current_app.config.get("JWT_SECRET_KEY", "secret")

        try:
            payload = jwt.decode(token, secret, algorithms=["HS256"])
            g.current_user = payload
        except jwt.ExpiredSignatureError:
            return unauthorized_response("Token has expired. Please log in again.")
        except jwt.InvalidTokenError:
            return unauthorized_response("Invalid or corrupted token.")

        return f(*args, **kwargs)
    return decorated


def log_request_info(app):
    """Logs incoming request method, path, and client IP."""
    logger.debug(f"--> {request.method} {request.path} | Remote: {request.remote_addr}")


def add_custom_headers(response):
    """Adds standard headers to outgoing responses."""
    response.headers["X-Application"] = "CollabSphere-Flask-CleanArch"
    return response


def setup_middleware(app):
    """Configure request hooks and global error handlers on the Flask app."""
    @app.before_request
    def before_request():
        log_request_info(app)

    @app.after_request
    def after_request(response):
        return add_custom_headers(response)

    @app.errorhandler(CustomException)
    def handle_custom_exception(error):
        details = getattr(error, 'errors', None)
        return error_response(message=error.message, status_code=error.status_code, details=details)

    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(error):
        return error_response(message="Validation failed", status_code=422, details=error.messages)

    @app.errorhandler(404)
    def handle_not_found(error):
        return error_response(message="Requested endpoint not found", status_code=404)

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return error_response(message="Method not allowed for this route", status_code=405)

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        logger.exception(f"Unhandled server error: {error}")
        return error_response(message="An internal server error occurred", status_code=500)


# Keep backward compatibility with old function name
middleware = setup_middleware