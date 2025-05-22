from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config_by_name

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Configure LoginManager
login_manager.login_view = 'main.login'  # The route for the login page (blueprint_name.route_function_name)
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'  # Bootstrap class for flash messages

def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)
    # Load configuration from config.py
    app.config.from_object(config_by_name[config_name])

    # Initialize Flask extensions with the app instance
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import models here to ensure they are registered with SQLAlchemy before db operations
    # and for the user_loader callback.
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        """User loader callback for Flask-Login."""
        return User.query.get(int(user_id))

    # Register blueprints
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Shell context for Flask CLI
    @app.shell_context_processor
    def make_shell_context():
        # Import all models for easy access in flask shell
        from app.models import Transaction, SavingsGoal # Import other models
        return {'app': app, 'db': db, 'User': User, 'Transaction': Transaction, 'SavingsGoal': SavingsGoal}

    return app
