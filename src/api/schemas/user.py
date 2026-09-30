from marshmallow import Schema, fields


class UserRegisterRequestSchema(Schema):
    """Schema for user registration."""
    user_name = fields.Str(required=True)
    password = fields.Str(required=True)
    description = fields.Str(allow_none=True)


class UserLoginRequestSchema(Schema):
    """Schema for user login."""
    user_name = fields.Str(required=True)
    password = fields.Str(required=True)


class UserUpdateRequestSchema(Schema):
    """Schema for updating user profile."""
    user_name = fields.Str(allow_none=True)
    password = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    status = fields.Bool(allow_none=True)


class UserResponseSchema(Schema):
    """Schema for user representation in responses."""
    id = fields.Int(required=True)
    user_name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    status = fields.Bool(required=True)
    created_at = fields.Raw(allow_none=True)
    updated_at = fields.Raw(allow_none=True)


class AuthResponseSchema(Schema):
    """Schema for authentication responses with JWT token."""
    token = fields.Str(required=True)
    user = fields.Nested(UserResponseSchema, required=True)
