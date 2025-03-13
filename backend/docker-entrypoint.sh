#!/bin/bash
set -e

# Function to wait for the database to be ready
wait_for_db() {
    echo "Waiting for database to be ready..."
    # For PostgreSQL, use pg_isready
    if [[ "$DATABASE_URL" == postgresql* ]]; then
        # Extract host and port from DATABASE_URL (simplified)
        DB_HOST=$(echo $DATABASE_URL | sed -e 's/^.*@\([^:]*\).*$/\1/')
        DB_PORT=$(echo $DATABASE_URL | sed -e 's/^.*:\([0-9]*\)\/.*$/\1/')
        
        until pg_isready -h $DB_HOST -p $DB_PORT -U postgres; do
            echo "PostgreSQL is unavailable - sleeping"
            sleep 1
        done
    else
        # For other databases, just wait a bit
        sleep 3
    fi
    
    echo "Database is ready!"
}

# Run migrations if requested
if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
    # Wait for the database first
    wait_for_db
    
    echo "Running database migrations..."
    python migrate.py upgrade
    echo "Migrations completed."
fi

# Start the application
exec "$@" 