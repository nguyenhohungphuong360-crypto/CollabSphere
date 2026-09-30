from flask import Blueprint, request, jsonify, g
from services.auth_service import AuthService
from services.user_service import UserService
from infrastructure.repositories.user_repository import UserRepository
from api.schemas.user import UserRegisterRequestSchema, UserLoginRequestSchema, UserResponseSchema
from api.middleware import token_required

bp = Blueprint('auth', __name__, url_prefix='/auth')

user_repo = UserRepository()
auth_service = AuthService(user_repo)
user_service = UserService(user_repo)

register_schema = UserRegisterRequestSchema()
login_schema = UserLoginRequestSchema()
user_response_schema = UserResponseSchema()


@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    post:
      summary: Register a new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserRegisterRequest'
      tags:
        - Authentication
      responses:
        201:
          description: User registered successfully with JWT token
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthResponse'
        400:
          description: Validation error
        409:
          description: Username already exists
    """
    data = request.get_json() or {}
    validated = register_schema.load(data)
    result = auth_service.register(
        user_name=validated['user_name'],
        password=validated['password'],
        description=validated.get('description'),
    )
    return jsonify(result), 201


@bp.route('/login', methods=['POST'])
def login():
    """
    User login
    ---
    post:
      summary: Authenticate user and obtain JWT token
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserLoginRequest'
      tags:
        - Authentication
      responses:
        200:
          description: Authentication successful
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthResponse'
        401:
          description: Invalid username or password
    """
    data = request.get_json() or {}
    validated = login_schema.load(data)
    result = auth_service.login(
        user_name=validated['user_name'],
        password=validated['password']
    )
    return jsonify(result), 200


@bp.route('/me', methods=['GET'])
@token_required
def get_me():
    """
    Get current user profile
    ---
    get:
      summary: Get authenticated user profile
      security:
        - BearerAuth: []
      tags:
        - Authentication
      responses:
        200:
          description: Profile of authenticated user
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        401:
          description: Unauthorized / Token invalid
    """
    user_id = int(g.current_user['sub'])
    user = user_service.get_user(user_id)
    return jsonify(user_response_schema.dump(user)), 200