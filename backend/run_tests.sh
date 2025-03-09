#!/bin/bash

# Set the Python path to include both the current directory and the app directory
export PYTHONPATH=$PYTHONPATH:/app:/app/app

# Run the tests
cd /app
python -m pytest "$@"