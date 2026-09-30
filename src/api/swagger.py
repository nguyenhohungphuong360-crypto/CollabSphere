from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from api.schemas.todo import TodoRequestSchema, TodoResponseSchema
from api.schemas.course import CourseRequestSchema, CourseResponseSchema
from api.schemas.user import (
    UserRegisterRequestSchema,
    UserLoginRequestSchema,
    UserUpdateRequestSchema,
    UserResponseSchema,
    AuthResponseSchema,
)

spec = APISpec(
    title="CollabSphere Clean Architecture API",
    version="2.0.0",
    openapi_version="3.0.3",
    info={
        "description": "Enterprise-grade REST API implemented using Clean Architecture with Flask, SQLAlchemy, Marshmallow, and JWT authentication.",
        "contact": {
            "name": "CollabSphere Engineering Team",
        }
    },
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# Configure Bearer Authentication Security Scheme in Swagger
api_key_scheme = {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Enter your JWT token obtained from /auth/login or /auth/register",
}
spec.components.security_scheme("BearerAuth", api_key_scheme)

# Register Schemas for Automatic Swagger Model Generation
spec.components.schema("TodoRequest", schema=TodoRequestSchema)
spec.components.schema("TodoResponse", schema=TodoResponseSchema)

spec.components.schema("CourseRequest", schema=CourseRequestSchema)
spec.components.schema("CourseResponse", schema=CourseResponseSchema)

spec.components.schema("UserRegisterRequest", schema=UserRegisterRequestSchema)
spec.components.schema("UserLoginRequest", schema=UserLoginRequestSchema)
spec.components.schema("UserUpdateRequest", schema=UserUpdateRequestSchema)
spec.components.schema("UserResponse", schema=UserResponseSchema)
spec.components.schema("AuthResponse", schema=AuthResponseSchema)