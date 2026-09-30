class CustomException(Exception):
    """Base class for all custom domain exceptions in the application."""
    status_code: int = 400

    def __init__(self, message: str = "An error occurred", status_code: int = None):
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self) -> dict:
        return {"error": self.message}


class NotFoundException(CustomException):
    """Exception raised when a requested resource is not found."""
    status_code = 404

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class ValidationException(CustomException):
    """Exception raised for validation errors."""
    status_code = 422

    def __init__(self, message: str = "Validation error", errors: dict = None):
        super().__init__(message, status_code=422)
        self.errors = errors or {}

    def to_dict(self) -> dict:
        result = {"error": self.message}
        if self.errors:
            result["details"] = self.errors
        return result


class UnauthorizedException(CustomException):
    """Exception raised for unauthorized access or authentication failure."""
    status_code = 401

    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, status_code=401)


class ForbiddenException(CustomException):
    """Exception raised for forbidden access."""
    status_code = 403

    def __init__(self, message: str = "Access forbidden"):
        super().__init__(message, status_code=403)


class ConflictException(CustomException):
    """Exception raised for duplicate or conflicting resources."""
    status_code = 409

    def __init__(self, message: str = "Resource conflict occurred"):
        super().__init__(message, status_code=409)