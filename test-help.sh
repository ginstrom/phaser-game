#!/bin/bash

# test-help.sh - Quick reference for test commands in the Phaser Game project

cat << 'EOF'
=======================================================
  PHASER GAME TEST COMMANDS QUICK REFERENCE
=======================================================

FRONTEND TESTS:
  ./test.sh frontend             # Run frontend tests
  ./test.sh frontend --watch     # Run frontend tests in watch mode
  ./test.sh frontend --coverage  # Run frontend tests with coverage

BACKEND TESTS:
  ./test.sh backend              # Run backend tests
  ./test.sh backend --verbose    # Run backend tests with verbose output
  ./test.sh backend --coverage   # Run backend tests with coverage

ALL TESTS:
  ./test.sh all                  # Run all tests

DOCUMENTATION:
  For more detailed information, see:
  - docs/TestingGuide.md
  - README.md (Testing section)

IMPORTANT:
  Always use the test.sh script for running tests.
  Do NOT run tests directly with npm or pytest.
=======================================================
EOF

echo "For more information, run: less docs/TestingGuide.md"