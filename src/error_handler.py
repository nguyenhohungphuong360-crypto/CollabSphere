# Error handling logic for the Flask application
from api.responses import error_response
from domain.exceptions import CustomException
from marshmallow import ValidationError
import logging

from flask import jsonify
logger = logging.getLogger(__name__)

class CustomError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__(message)
        if status_code is not None:
            self.status_code = status_code
        self.message = message
def register_error_handlers(app):
    """Register custom error handlers for the application."""

    def to_dict(self):
        return {'message': self.message}
    @app.errorhandler(CustomException)
    def handle_custom_exception(error):
        details = getattr(error, 'errors', None)
        return error_response(message=error.message, status_code=error.status_code, details=details)

def handle_error(error):
    if isinstance(error, CustomError):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return error_response(message="Validation failed", status_code=422, details=error.messages)

    response = jsonify({'message': 'An unexpected error occurred.'})
    response.status_code = 500
    return response

def register_error_handlers(app):
    app.register_error_handler(Exception, handle_error)
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        logger.exception(f"Unexpected error: {error}")
        return error_response(message="An unexpected error occurred.", status_code=500)