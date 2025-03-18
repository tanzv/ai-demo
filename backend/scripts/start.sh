#!/bin/bash

# Default values
ENV="development"
HOST="0.0.0.0"
PORT="8000"
DEBUG=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --env=*)
            ENV="${1#*=}"
            shift
            ;;
        --host=*)
            HOST="${1#*=}"
            shift
            ;;
        --port=*)
            PORT="${1#*=}"
            shift
            ;;
        --debug)
            DEBUG="--debug"
            shift
            ;;
        *)
            echo "Unknown parameter: $1"
            exit 1
            ;;
    esac
done

# Create logs directory if it doesn't exist
mkdir -p logs

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Export environment variables
export PYTHONPATH=$PYTHONPATH:$(pwd)
export FLASK_APP=backend.app:create_app
export FLASK_ENV=$ENV

# Run the application
python run.py --env=$ENV --host=$HOST --port=$PORT $DEBUG 