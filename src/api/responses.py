# src/api/responses.py

from flask import jsonify
from typing import Any, Optional

def success_response(data, message="Success"):
    return jsonify({"message": message, "data": data}), 200

def error_response(message="An error occurred", status_code=400):
    return jsonify({"message": message}), status_code
def success_response(data: Any = None, message: str = "Success", status_code: int = 200):
    """Generate a standard success JSON response."""
    payload = {
        "success": True,
        "message": message,
    }
    if data is not None:
        payload["data"] = data
    return jsonify(payload), status_code

def not_found_response(message="Resource not found"):
    return jsonify({"message": message}), 404

def validation_error_response(errors):
    return jsonify({"message": "Validation errors", "errors": errors}), 422
def error_response(message: str = "An error occurred", status_code: int = 400, details: Any = None):
    """Generate a standard error JSON response."""
    payload = {
        "success": False,
        "error": message,
    }
    if details is not None:
        payload["details"] = details
    return jsonify(payload), status_code


def not_found_response(message: str = "Resource not found"):
    return error_response(message=message, status_code=404)


def validation_error_response(errors: Any, message: str = "Validation failed"):
    return error_response(message=message, status_code=422, details=errors)


def unauthorized_response(message: str = "Unauthorized access"):
    return error_response(message=message, status_code=401)