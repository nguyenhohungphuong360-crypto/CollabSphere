from flask import Blueprint, request, jsonify
from services.user_service import UserService
from infrastructure.repositories.user_repository import UserRepository
from api.schemas.user import UserResponseSchema, UserUpdateRequestSchema
from api.middleware import token_required

bp = Blueprint('user', __name__, url_prefix='/users')

user_service = UserService(UserRepository())
response_schema = UserResponseSchema()
update_schema = UserUpdateRequestSchema()


@bp.route('/', methods=['GET'])
def list_users():
    """
    Get all users
    ---
    get:
      summary: List all users
      tags:
        - Users
      responses:
        200:
          description: List of users
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/UserResponse'
    """
    users = user_service.list_users()
    return jsonify(response_schema.dump(users, many=True)), 200


@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get user by id
    ---
    get:
      summary: Get user by ID
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
          description: User ID
      tags:
        - Users
      responses:
        200:
          description: User details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        404:
          description: User not found
    """
    user = user_service.get_user(user_id)
    return jsonify(response_schema.dump(user)), 200


@bp.route('/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    """
    Update user
    ---
    put:
      summary: Update user profile
      security:
        - BearerAuth: []
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
          description: User ID
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserUpdateRequest'
      tags:
        - Users
      responses:
        200:
          description: User updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        404:
          description: User not found
    """
    data = request.get_json() or {}
    validated = update_schema.load(data)
    user = user_service.update_user(
        user_id=user_id,
        user_name=validated.get('user_name'),
        password=validated.get('password'),
        description=validated.get('description'),
        status=validated.get('status'),
    )
    return jsonify(response_schema.dump(user)), 200


@bp.route('/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    """
    Delete user
    ---
    delete:
      summary: Delete user by ID
      security:
        - BearerAuth: []
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
          description: User ID
      tags:
        - Users
      responses:
        204:
          description: User deleted successfully
        404:
          description: User not found
    """
    user_service.delete_user(user_id)
    return '', 204
