from flask import Flask, jsonify
from flask_cors import CORS
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException
from config.settings import settings
from models.user import User

login_manager = LoginManager()

def create_app():
    """Create Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.update(
        SECRET_KEY=settings.get('auth.secret_key'),
        SQLALCHEMY_DATABASE_URI=settings.database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_POOL_SIZE=settings.get('database.pool_size', 5),
        SQLALCHEMY_POOL_RECYCLE=settings.get('database.pool_recycle', 3600),
        JWT_SECRET_KEY=settings.get('auth.jwt_secret_key'),
        JWT_ACCESS_TOKEN_EXPIRES=settings.get('auth.access_token_expires'),
        JWT_REFRESH_TOKEN_EXPIRES=settings.get('auth.refresh_token_expires')
    )
    
    # Initialize extensions
    from config.database import init_db
    init_db(app)
    
    # Initialize login manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Initialize CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": settings.get('cors.origins', "*"),
            "methods": settings.get('cors.allow_methods', ["GET", "POST", "PUT", "DELETE", "OPTIONS"]),
            "allow_headers": settings.get('cors.allow_headers', ["Content-Type", "Authorization"]),
            "supports_credentials": True
        }
    })
    
    # Register error handlers
    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        """Handle HTTP errors"""
        response = {
            "error": error.name,
            "message": error.description,
            "status_code": error.code
        }
        return jsonify(response), error.code

    @app.errorhandler(Exception)
    def handle_error(error):
        """Handle non-HTTP errors"""
        app.logger.error(f"An error occurred: {error}")
        response = {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "status_code": 500
        }
        return jsonify(response), 500
    
    # Register blueprints
    from api.v1.endpoints.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix=f"{settings.get('project.api_prefix', '/api/v1')}/auth")
    
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "version": app.config.get('VERSION', '0.1.0')
        })
    
    return app 