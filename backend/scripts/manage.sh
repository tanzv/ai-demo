#!/bin/bash

# Function to create virtual environment and install dependencies
setup_env() {
    echo "Creating virtual environment..."
    uv venv
    source .venv/bin/activate
    
    echo "Installing dependencies..."
    uv pip install -e .
    
    echo "Installing development dependencies..."
    uv pip install -e pyproject.dev.toml
}

# Function to run the application
run_app() {
    source .venv/bin/activate
    python -m backend.main
}

# Function to run tests
run_tests() {
    source .venv/bin/activate
    pytest
}

# Function to lint code
lint_code() {
    source .venv/bin/activate
    ruff check .
    ruff format .
}

# Function to clean project
clean_project() {
    rm -rf .venv
    rm -rf __pycache__
    rm -rf .pytest_cache
    rm -rf .coverage
    rm -rf htmlcov
    rm -rf dist
    rm -rf build
    rm -rf *.egg-info
    find . -type d -name "__pycache__" -exec rm -r {} +
}

# Main script
case "$1" in
    "setup")
        setup_env
        ;;
    "run")
        run_app
        ;;
    "test")
        run_tests
        ;;
    "lint")
        lint_code
        ;;
    "clean")
        clean_project
        ;;
    *)
        echo "Usage: $0 {setup|run|test|lint|clean}"
        exit 1
        ;;
esac

exit 0 