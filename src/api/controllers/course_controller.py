from flask import Blueprint, request, jsonify
from services.course_service import CourseService
from infrastructure.repositories.course_repository import CourseRepository
from api.schemas.course import CourseRequestSchema, CourseResponseSchema

bp = Blueprint('course', __name__, url_prefix='/courses')

course_service = CourseService(CourseRepository())
request_schema = CourseRequestSchema()
response_schema = CourseResponseSchema()


@bp.route('/', methods=['GET'])
def list_courses():
    """
    Get all courses
    ---
    get:
      summary: Get all courses
      tags:
        - Courses
      responses:
        200:
          description: List of courses
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/CourseResponse'
    """
    courses = course_service.list_courses()
    data = response_schema.dump(courses, many=True)
    return jsonify(data), 200


@bp.route('/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """
    Get course by id
    ---
    get:
      summary: Get course by id
      parameters:
        - name: course_id
          in: path
          required: true
          schema:
            type: integer
          description: Course ID
      tags:
        - Courses
      responses:
        200:
          description: Course details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CourseResponse'
        404:
          description: Course not found
    """
    course = course_service.get_course(course_id)
    return jsonify(response_schema.dump(course)), 200


@bp.route('/', methods=['POST'])
def create_course():
    """
    Create a new course
    ---
    post:
      summary: Create a new course
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CourseRequest'
      tags:
        - Courses
      responses:
        201:
          description: Course created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CourseResponse'
        400:
          description: Invalid input or validation failed
    """
    data = request.get_json() or {}
    validated = request_schema.load(data)
    course = course_service.create_course(
        course_name=validated['course_name'],
        description=validated.get('description'),
        status=validated.get('status', 'active'),
        start_date=validated.get('start_date'),
        end_date=validated.get('end_date'),
    )
    return jsonify(response_schema.dump(course)), 201


@bp.route('/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """
    Update a course by id
    ---
    put:
      summary: Update a course by id
      parameters:
        - name: course_id
          in: path
          required: true
          schema:
            type: integer
          description: Course ID to update
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CourseRequest'
      tags:
        - Courses
      responses:
        200:
          description: Course updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CourseResponse'
        404:
          description: Course not found
        400:
          description: Invalid input
    """
    data = request.get_json() or {}
    validated = request_schema.load(data)
    course = course_service.update_course(
        course_id=course_id,
        course_name=validated['course_name'],
        description=validated.get('description'),
        status=validated.get('status', 'active'),
        start_date=validated.get('start_date'),
        end_date=validated.get('end_date'),
    )
    return jsonify(response_schema.dump(course)), 200


@bp.route('/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """
    Delete a course by id
    ---
    delete:
      summary: Delete a course by id
      parameters:
        - name: course_id
          in: path
          required: true
          schema:
            type: integer
          description: Course ID to delete
      tags:
        - Courses
      responses:
        204:
          description: Course deleted successfully
        404:
          description: Course not found
    """
    course_service.delete_course(course_id)
    return '', 204