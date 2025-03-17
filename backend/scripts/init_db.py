from sqlalchemy.orm import Session
from backend.config.database import SessionLocal, engine, Base
from backend.config.settings import settings
from backend.models.user import User
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def init_db() -> None:
    """Initialize database with default admin user"""
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if admin user already exists
        user = db.query(User).filter(
            User.username == settings.get('admin.username')
        ).first()
        
        if not user:
            # Create default admin user
            admin = User(
                username=settings.get('admin.username'),
                email=settings.get('admin.email'),
                hashed_password=User.get_password_hash(
                    settings.get('admin.password')
                ),
                is_superuser=True
            )
            db.add(admin)
            db.commit()
            print("Created default admin user")
        else:
            print("Admin user already exists")
            
    finally:
        db.close()

def init_postgres_db():
    """Initialize PostgreSQL database if not exists"""
    # Connect to PostgreSQL server
    conn = psycopg2.connect(
        host=settings.get('database.host'),
        user=settings.get('database.user'),
        password=settings.get('database.password')
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Check if database exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", 
                  (settings.get('database.db_name'),))
    exists = cursor.fetchone()
    
    if not exists:
        try:
            cursor.execute(f"CREATE DATABASE {settings.get('database.db_name')}")
            print(f"Database {settings.get('database.db_name')} created successfully")
        except Exception as e:
            print(f"Error creating database: {e}")
            return False
    
    cursor.close()
    conn.close()
    return True

def create_admin_user(app):
    """Create admin user if not exists"""
    from backend.models.user import User
    from backend.config.database import db
    
    with app.app_context():
        # Check if admin user exists
        admin = User.query.filter_by(
            username=settings.get('admin.username')
        ).first()
        
        if not admin:
            # Create admin user
            admin = User(
                username=settings.get('admin.username'),
                email=settings.get('admin.email'),
                is_superuser=True
            )
            admin.set_password(settings.get('admin.password'))
            
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully")
        else:
            print("Admin user already exists")

def init_app(app):
    """Initialize application database and admin user"""
    if init_postgres_db():
        from backend.config.database import init_db
        init_db(app)
        create_admin_user(app)
        print("Database initialization completed")

if __name__ == "__main__":
    print("Creating initial data")
    init_db()
    print("Initial data created") 