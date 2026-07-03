"""Flask application factory"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_session import Session
import os
import logging

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='development'):
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    if config_name == 'production':
        from app.config import ProductionConfig
        app.config.from_object(ProductionConfig)
    else:
        from app.config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    Session(app)
    
    # Create necessary folders
    os.makedirs(app.config.get('DOWNLOAD_FOLDER', './downloads'), exist_ok=True)
    os.makedirs(app.config.get('TEMP_FOLDER', './temp'), exist_ok=True)
    os.makedirs(app.config.get('LOGS_FOLDER', './logs'), exist_ok=True)
    
    # Setup logging
    setup_logging(app)
    
    # Register blueprints
    with app.app_context():
        from app.routes import auth_bp, videos_bp, queue_bp, upload_bp, settings_bp, logs_bp, health_bp
        
        app.register_blueprint(auth_bp.bp)
        app.register_blueprint(videos_bp.bp)
        app.register_blueprint(queue_bp.bp)
        app.register_blueprint(upload_bp.bp)
        app.register_blueprint(settings_bp.bp)
        app.register_blueprint(logs_bp.bp)
        app.register_blueprint(health_bp.bp)
        
        # Create tables
        db.create_all()
    
    return app

def setup_logging(app):
    """Configure logging"""
    log_folder = app.config.get('LOGS_FOLDER', './logs')
    os.makedirs(log_folder, exist_ok=True)
    
    log_file = os.path.join(log_folder, 'app.log')
    
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
