#!/bin/bash
set -e

echo "Starting backend service via docker-compose..."
docker-compose up -d backend

echo "Waiting for the backend service to initialize..."
sleep 5

echo "Executing functional tests on the backend..."
pytest backend/functional_tests
