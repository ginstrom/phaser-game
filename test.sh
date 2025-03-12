#!/bin/bash

# test.sh - A script to run unit tests for the Phaser game project
# Usage: ./test.sh [frontend|backend|all|cli] [options]
# Options:
#   --watch     Run tests in watch mode (frontend only)
#   --coverage  Generate test coverage report
#   --verbose   Run tests with verbose output (backend only)
#   --help      Display this help message

# Display usage information
show_usage() {
    echo "Usage: ./test.sh [frontend|backend|all|cli] [options]"
    echo ""
    echo "Arguments:"
    echo "  frontend   Run frontend tests"
    echo "  backend    Run backend tests"
    echo "  all        Run both frontend and backend tests"
    echo "  cli        Start interactive CLI for debugging the backend API"
    echo ""
    echo "Options:"
    echo "  --watch     Run tests in watch mode (frontend only)"
    echo "  --coverage  Generate test coverage report"
    echo "  --verbose   Run tests with verbose output (backend only)"
    echo "  --help      Display this help message"
    exit 1
}

# Check if argument is provided
if [ $# -eq 0 ]; then
    show_usage
fi

# Parse command line arguments
TEST_TARGET=""
WATCH_MODE=false
COVERAGE_MODE=false
VERBOSE_MODE=false

for arg in "$@"; do
    case $arg in
        frontend|backend|all|cli)
            if [ -z "$TEST_TARGET" ]; then
                TEST_TARGET=$arg
            else
                echo "Error: Multiple test targets specified."
                show_usage
            fi
            ;;
        --watch)
            WATCH_MODE=true
            ;;
        --coverage)
            COVERAGE_MODE=true
            ;;
        --verbose)
            VERBOSE_MODE=true
            ;;
        --help)
            show_usage
            ;;
        *)
            echo "Error: Unknown argument '$arg'"
            show_usage
            ;;
    esac
done

# Run tests based on arguments
run_frontend_tests() {
    echo "Running frontend tests..."
    
    if [ "$WATCH_MODE" = true ] && [ "$COVERAGE_MODE" = true ]; then
        echo "Error: Cannot use both --watch and --coverage options together."
        exit 1
    elif [ "$WATCH_MODE" = true ]; then
        docker-compose -f docker-compose.test.yml run frontend-watch
    elif [ "$COVERAGE_MODE" = true ]; then
        docker-compose -f docker-compose.test.yml run frontend-coverage
    else
        docker-compose -f docker-compose.test.yml run frontend
    fi
}

run_backend_tests() {
    echo "Running backend tests..."
    
    if [ "$WATCH_MODE" = true ]; then
        echo "Warning: Watch mode is not supported for backend tests."
    fi
    
    if [ "$VERBOSE_MODE" = true ] && [ "$COVERAGE_MODE" = true ]; then
        echo "Error: Cannot use both --verbose and --coverage options together."
        exit 1
    elif [ "$VERBOSE_MODE" = true ]; then
        docker-compose -f docker-compose.test.yml run backend-verbose
    elif [ "$COVERAGE_MODE" = true ]; then
        docker-compose -f docker-compose.test.yml run backend-coverage
    else
        docker-compose -f docker-compose.test.yml run backend
    fi
}

run_cli() {
    echo "Starting backend API and CLI..."
    # Ensure services are up
    docker-compose -f docker-compose.test.yml up -d db
    # Wait for database to be ready
    echo "Waiting for database to be ready..."
    sleep 3
    # Initialize database
    echo "Initializing database..."
    docker-compose -f docker-compose.test.yml run --rm backend python -c "from app.db.init_db import init_db; init_db()"
    # Start backend API
    docker-compose -f docker-compose.test.yml up -d backend-api
    # Wait for backend to be ready
    echo "Waiting for backend API to be ready..."
    sleep 5
    # Run CLI
    docker-compose -f docker-compose.test.yml run --rm cli
}

# Execute tests based on target
case $TEST_TARGET in
    frontend)
        run_frontend_tests
        ;;
    backend)
        run_backend_tests
        ;;
    all)
        run_frontend_tests
        run_backend_tests
        ;;
    cli)
        run_cli
        ;;
    *)
        show_usage
        ;;
esac

if [ "$TEST_TARGET" != "cli" ]; then
    echo "Tests completed."
fi
