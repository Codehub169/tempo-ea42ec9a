#!/bin/bash

# Navigate to the project directory (optional, assumes script is run from project root)
# cd /path/to/your/project

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Set Flask environment variables
export FLASK_APP=run.py
export FLASK_ENV=development # Use 'production' for deployment
# For production, a more secure SECRET_KEY should be set as an environment variable
# export SECRET_KEY='your_production_secret_key'

# Initialize the database (if using Flask-Migrate)
# This will create the database file (e.g., site.db) if it doesn't exist
# and apply any pending migrations.
flask db init 2>/dev/null # Initialize migrations if not already done, suppress error if it is
flask db migrate -m "Initial migration" 2>/dev/null # Create migration, suppress error if no changes
flask db upgrade # Apply migrations

echo "Starting the Flask application on port 9000..."
# Run the Flask application on port 9000
flask run --host=0.0.0.0 --port=9000

# Deactivate virtual environment upon exit (optional)
# deactivate
