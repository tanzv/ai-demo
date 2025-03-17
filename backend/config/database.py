from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import settings
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Get database URL from configuration manager
engine = create_engine(
    settings.database_url,
    pool_size=settings.get('database.pool_size', 5),
    pool_recycle=settings.get('database.pool_recycle', 3600)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

db = SQLAlchemy()
migrate = Migrate()

def get_db():
    """
    Database dependency to be used in FastAPI endpoints
    Yields a database session and ensures it's closed after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db(app):
    """Initialize database with Flask application"""
    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_POOL_SIZE'] = settings.get('database.pool_size', 5)
    app.config['SQLALCHEMY_POOL_RECYCLE'] = settings.get('database.pool_recycle', 3600)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models here to ensure they are registered with SQLAlchemy
    from backend.models.user import User  # noqa
    
    # Create tables
    with app.app_context():
        db.create_all() 