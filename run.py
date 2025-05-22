import os
from app import create_app, db # Assuming create_app is in app/__init__.py
from app.models import User, Transaction, SavingsGoal # Import models to ensure they are known to Flask-Migrate
from flask_migrate import Migrate

# Determine the configuration name from an environment variable or default to 'development'
config_name = os.getenv('FLASK_CONFIG', 'development')

app = create_app(config_name)

# Initialize Flask-Migrate
# The Migrate instance needs both the app and the db
migrate = Migrate(app, db)

# This allows running the app with 'python run.py'
if __name__ == '__main__':
    # Ensure the instance folder exists where SQLite DB will be stored
    instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
    
    # The port and host are configured in startup.sh via 'flask run' command arguments.
    # If running directly with 'python run.py', you might want to specify them here:
    # app.run(host='0.0.0.0', port=9000, debug=app.config['DEBUG'])
    # However, the standard way with FLASK_APP set is to use 'flask run'.
    # For simplicity and consistency with startup.sh, we'll rely on 'flask run'.
    
    # The following is mostly for completeness if one were to run `python run.py` directly
    # and wanted to ensure the app context is available for shell commands or similar.
    # For typical `flask run` usage, this direct `app.run()` call isn't strictly necessary
    # as `flask run` handles it.
    if os.getenv('FLASK_ENV') == 'development' or app.config['DEBUG']:
        app.run(host='0.0.0.0', port=9000)
    else:
        # In a production scenario, you might use a proper WSGI server like Gunicorn or Waitress.
        # For simplicity with the current setup, this direct run is kept, but 'flask run' is preferred.
        app.run(host='0.0.0.0', port=9000)
