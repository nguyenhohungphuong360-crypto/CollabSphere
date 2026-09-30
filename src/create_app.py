import logging
from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

from config import Config
from cors import init_cors
from app_logging import setup_logging
from infrastructure.databases import init_db
from api.middleware import setup_middleware
from api.swagger import spec

# Import controllers
from api.controllers.todo_controller import bp as todo_bp
from api.controllers.course_controller import bp as course_bp
from api.controllers.auth_controller import bp as auth_bp
from api.controllers.user_controller import bp as user_bp

logger = logging.getLogger(__name__)


def create_app(config_class=Config):
    """Application factory for Flask Clean Architecture application."""
    setup_logging()

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize CORS
    init_cors(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(todo_bp)

    # Setup Swagger UI
    SWAGGER_URL = '/docs'
    API_URL = '/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "CollabSphere Clean Architecture API",
            'persistAuthorization': True,
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Initialize Database & tables
    try:
        init_db(app)
    except Exception as e:
        logger.error(f"Error initializing database: {e}")

    # Register Middleware & Error Handlers
    setup_middleware(app)

    # Root endpoint
    @app.route("/", methods=["GET"])
    def index():
        return jsonify({
            "name": "CollabSphere Clean Architecture API",
            "version": "2.0.0",
            "status": "running",
            "documentation": "/docs",
            "endpoints": {
                "auth": "/auth",
                "users": "/users",
                "courses": "/courses",
                "todos": "/todos"
            }
        }), 200

    # Auto-register view paths to APISpec
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint.startswith(('todo.', 'course.', 'auth.', 'user.')):
                view_func = app.view_functions[rule.endpoint]
                try:
                    spec.path(view=view_func)
                except Exception as e:
                    logger.debug(f"Note on Swagger path registration for {rule.endpoint}: {e}")

    @app.route("/swagger.json", methods=["GET"])
    def swagger_json():
        return jsonify(spec.to_dict())

    return app