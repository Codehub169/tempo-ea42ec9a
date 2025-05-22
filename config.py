import os

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key_for_development_12345'
    # For SQLite, the path can be relative to the instance folder or an absolute path.
    # Using os.path.join to ensure cross-platform compatibility.
    # The database file will be created in an 'instance' folder at the root of the project.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True # Enable debug mode for development

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    # In development, you might want a more predictable secret key
    # SECRET_KEY = 'dev_secret_key'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # Ensure SECRET_KEY is set via environment variable in production
    # SQLALCHEMY_DATABASE_URI might also be set via environment variable for a production database

# Dictionary to access configurations by name, e.g., 'development', 'production'
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
