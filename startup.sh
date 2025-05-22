#!/bin/bash

# Exit script on error, treat unset variables as an error, and ensure pipeline errors are caught.
set -euo pipefail

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# Activate the virtual environment
# Note: 'source' might not be available in all non-interactive shells.
# For cron jobs or similar, ensure the shell supports it or use an absolute path to activate.
source venv/bin/activate

# Install dependencies
if [ -f "requirements.txt" ]; then
  echo "Installing dependencies from requirements.txt..."
  pip install -r requirements.txt
else
  echo "WARNING: requirements.txt not found. Skipping dependency installation."
fi

# Set Flask environment variables
export FLASK_APP=run.py
# Use FLASK_ENV from environment if set, otherwise default to 'development'
export FLASK_ENV=${FLASK_ENV:-development}
# For production, a more secure SECRET_KEY should be set as an environment variable.
# config.py uses a default development key if SECRET_KEY is not set in the environment.

# Ensure the instance folder exists (for SQLite database)
echo "Ensuring instance folder exists..."
mkdir -p instance

# Initialize the database and apply migrations
echo "Preparing database..."
# Initialize migrations directory only if it doesn't exist.
if [ ! -d "migrations" ]; then
    echo "Flask-Migrate 'migrations' folder not found. Initializing..."
    flask db init
    echo "Attempting to create initial schema migration..."
    # This tries to create an initial migration. It might 'fail' (non-zero exit code)
    # if no models are defined yet or if (less likely after fresh init) no changes are detected.
    # The '2>/dev/null' silences output. The '|| echo ...' runs if the command fails,
    # preventing 'set -e' from stopping the script for benign 'failures'.
    flask db migrate -m "Initial schema creation" 2>/dev/null || echo "No initial migration created or models not yet defined. This is usually OK for a first run."
fi

echo "Applying database migrations..."
# This will apply any pending migrations to the database.
# If this command fails (e.g., database not reachable, error in migration script),
# the script will exit due to 'set -e'.
flask db upgrade

echo "Starting the Flask application on port 9000..."
# Run the Flask application using Flask's built-in development server.
# The host 0.0.0.0 makes it accessible from any IP address on the network.
# For production deployments, a dedicated WSGI server (e.g., Gunicorn, uWSGI) is recommended.
flask run --host=0.0.0.0 --port=9000

# Deactivate virtual environment upon exit (optional, as the script's environment ends upon exit anyway)
# deactivate
