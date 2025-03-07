#!/bin/bash

# test.sh - A script to run unit tests for the Phaser game project
# Usage: ./test.sh [frontend|backend|all] [options]
# Options:
#   --watch     Run tests in watch mode (frontend only)
#   --coverage  Generate test coverage report
#   --verbose   Run tests with verbose output (backend only)
#   --help      Display this help message

# Display usage information
show_usage() {
    echo "Usage: ./test.sh [frontend|backend|all] [options]"
    echo ""
    echo "Arguments:"
    echo "  frontend   Run frontend tests"
    echo "  backend    Run backend tests"
    echo "  all        Run both frontend and backend tests"
    echo ""
    echo "Options:"
    echo "  --watch     Run tests in watch mode (frontend only)"
    echo "  --coverage  Generate test coverage report"
    echo "  --verbose   Run tests with verbose output (backend only)"
    echo "  --help      Display this help message"
    echo ""
    echo "Examples:"
    echo "  ./test.sh frontend             # Run frontend tests"
    echo "  ./test.sh backend --verbose    # Run backend tests with verbose output"
    echo "  ./test.sh frontend --coverage  # Run frontend tests with coverage report"
    echo "  ./test.sh all                  # Run both frontend and backend tests"
}

# Check if no arguments were provided
if [ $# -eq 0 ]; then
    echo "Error: No arguments provided."
    show_usage
    exit 1
fi

# Parse command line arguments
TEST_TARGET=""
WATCH_MODE=false
COVERAGE_MODE=false
VERBOSE_MODE=false

for arg in "$@"; do
    case $arg in
        frontend|backend|all)
            if [ -z "$TEST_TARGET" ]; then
                TEST_TARGET=$arg
            else
                echo "Error: Multiple test targets specified. Please specify only one of: frontend, backend, or all."
                show_usage
                exit 1
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
            exit 0
            ;;
        *)
            echo "Error: Unknown argument '$arg'"
            show_usage
            exit 1
            ;;
    esac
done

# Validate test target
if [ -z "$TEST_TARGET" ]; then
    echo "Error: No test target specified. Please specify one of: frontend, backend, or all."
    show_usage
    exit 1
fi

# Run tests based on arguments
run_frontend_tests() {
    echo "Running frontend tests..."
    
    if [ "$WATCH_MODE" = true ] && [ "$COVERAGE_MODE" = true ]; then
        echo "Error: Cannot use both --watch and --coverage options together for frontend tests."
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
        echo "Warning: Watch mode is not supported for backend tests. Ignoring --watch option."
    fi
    
    if [ "$VERBOSE_MODE" = true ] && [ "$COVERAGE_MODE" = true ]; then
        echo "Error: Cannot use both --verbose and --coverage options together for backend tests."
        exit 1
    elif [ "$VERBOSE_MODE" = true ]; then
        docker-compose -f docker-compose.test.yml run backend-verbose
    elif [ "$COVERAGE_MODE" = true ]; then
        docker-compose -f docker-compose.test.yml run backend-coverage
    else
        docker-compose -f docker-compose.test.yml run backend
    fi
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
esac

echo "Tests completed."
