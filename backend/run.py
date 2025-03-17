import os
import argparse
from backend.app import create_app
from backend.scripts.init_db import init_app

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Run AI Demo Application')
    parser.add_argument(
        '--env',
        default='development',
        choices=['development', 'production', 'testing'],
        help='Environment to run the application in'
    )
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host to run the application on'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Port to run the application on'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Run in debug mode'
    )
    return parser.parse_args()

def setup_environment(env):
    """Setup environment variables"""
    os.environ['ENV'] = env
    os.environ['FLASK_ENV'] = env
    
    # Set config path based on environment
    config_path = f'backend/config/{env}.yaml'
    if os.path.exists(config_path):
        os.environ['CONFIG_PATH'] = config_path
    else:
        os.environ['CONFIG_PATH'] = 'backend/config/default.yaml'

def main():
    """Main entry point"""
    args = parse_args()
    
    # Setup environment
    setup_environment(args.env)
    
    # Create and configure app
    app = create_app()
    
    # Initialize database
    init_app(app)
    
    # Set debug mode based on environment and args
    debug = args.debug or args.env == 'development'
    
    # Run application
    app.run(
        host=args.host,
        port=args.port,
        debug=debug,
        use_reloader=debug
    )

if __name__ == '__main__':
    main() 