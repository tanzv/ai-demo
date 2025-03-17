from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from backend.config.settings import settings
from backend.models.user import User

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
        SQLALCHEMY_POOL_RECYCLE=settings.get('database.pool_recycle', 3600)
    )
    
    # Initialize extensions
    from backend.config.database import init_db
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
            "origins": settings.get('cors.origins'),
            "methods": settings.get('cors.allow_methods'),
            "allow_headers": settings.get('cors.allow_headers'),
            "supports_credentials": True
        }
    })
    
    # Register blueprints
    from backend.api.v1.endpoints.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix=f"{settings.get('project.api_prefix')}/auth")
    
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return {"status": "healthy"}
    
    return app 