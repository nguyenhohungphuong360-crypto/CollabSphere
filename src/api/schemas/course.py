from marshmallow import Schema, fields


class CourseRequestSchema(Schema):
    """Schema for creating or updating a course."""
    course_name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    status = fields.Str(load_default="active")
    start_date = fields.DateTime(allow_none=True)
    end_date = fields.DateTime(allow_none=True)


class CourseResponseSchema(Schema):
    """Schema for serializing a course response."""
    id = fields.Int(required=True)
    course_name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    status = fields.Str(required=True)
    start_date = fields.Raw(allow_none=True)
    end_date = fields.Raw(allow_none=True)
    created_at = fields.Raw(allow_none=True)
    updated_at = fields.Raw(allow_none=True)
