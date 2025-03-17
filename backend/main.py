from backend.app import create_app
from backend.scripts.init_db import init_app

def main():
    """Main function to start the application"""
    app = create_app()
    
    # Initialize database and create admin user
    init_app(app)
    
    # Start the application
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )

if __name__ == "__main__":
    main() 