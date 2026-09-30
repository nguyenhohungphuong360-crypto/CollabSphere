from marshmallow import Schema, fields


class TodoRequestSchema(Schema):
    """Schema for creating or updating a todo item."""
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    status = fields.Str(required=True)
    description = fields.Str(required=False, allow_none=True, load_default=None)
    status = fields.Str(required=False, load_default="pending")


class TodoResponseSchema(Schema):
    """Schema for serializing a todo item response."""
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    status = fields.Str(required=True)
    created_at = fields.Raw(required=True)
    updated_at = fields.Raw(required=True) 
    created_at = fields.Raw(allow_none=True)
    updated_at = fields.Raw(allow_none=True)