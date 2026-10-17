#!/usr/bin/env python3
"""Le Chonk - Cat Health & Weight Tracker

A lightweight Flask application for tracking cat weights, vaccinations, and documents.

Usage:
    python run.py        # Run in development mode
    python run.py prod   # Run in production mode (not recommended without proper setup)
"""

from app import create_app
import os

# Determine config based on environment
if os.environ.get('FLASK_ENV') == 'production' or 'prod' in os.sys.argv:
    app = create_app('config.ProductionConfig')
else:
    app = create_app()

if __name__ == '__main__':
    # Determine host and port
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    
    print(f" * Running Le Chonk on http://{host}:{port}")
    print(f" * Debug mode: {'ON' if debug else 'OFF'}")
    print(f" * Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    app.run(host=host, port=port, debug=debug)
