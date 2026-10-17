import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Determine the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    # Secret key for session management - CHANGE THIS IN PRODUCTION
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-me'
    
    # Database configuration
    # Default: SQLite database in instance/lechonk.db
    # Can be overridden by DATABASE_URL environment variable or .env file
    # Example: sqlite:////absolute/path/to/database.db
    #          postgresql://user:password@localhost/dbname
    DEFAULT_DB_PATH = os.path.join(BASE_DIR, 'instance', 'lechonk.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{DEFAULT_DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload configuration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'webp', 'svg', 'bmp'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
