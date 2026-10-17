from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import json
import re

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()


def load_config():
    """Load configuration from lechonk_config.json if it exists"""
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lechonk_config.json')
    config = {}
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except Exception:
            config = {}
    return config


def ensure_db_directory(db_uri):
    """Ensure the directory for the database file exists"""
    # For SQLite file-based databases
    if db_uri.startswith('sqlite:///'):
        # Extract the path after sqlite:///
        db_path = db_uri.replace('sqlite:///', '')
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)


def create_app(config_class='config.Config'):
    """Application factory"""
    from config import Config
    
    app = Flask(__name__)
    
    # Load custom config from file
    custom_config = load_config()
    
    # Apply configuration
    app.config.from_object(config_class)
    
    # Override with custom config from file
    if custom_config.get('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = custom_config['DATABASE_URL']
    
    if custom_config.get('UPLOAD_FOLDER'):
        # Use absolute path if provided, otherwise join with base dir
        upload_path = custom_config['UPLOAD_FOLDER']
        if not os.path.isabs(upload_path):
            # If relative path, join with the application's parent directory
            app.config['UPLOAD_FOLDER'] = os.path.join(
                os.path.dirname(app.root_path), 
                upload_path
            )
        else:
            app.config['UPLOAD_FOLDER'] = upload_path
    
    # Ensure all necessary directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    ensure_db_directory(app.config['SQLALCHEMY_DATABASE_URI'])
    
    # Set max content length
    app.config['MAX_CONTENT_LENGTH'] = app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    return app
