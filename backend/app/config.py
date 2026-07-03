"""Application configuration"""

import os
from datetime import timedelta

class BaseConfig:
    """Base configuration"""
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_PERMANENT = False
    SESSION_TYPE = 'filesystem'
    
    # Folders
    DOWNLOAD_FOLDER = os.getenv('DOWNLOAD_FOLDER', './downloads')
    TEMP_FOLDER = os.getenv('TEMP_FOLDER', './temp')
    LOGS_FOLDER = os.getenv('LOGS_FOLDER', './logs')
    
    # YouTube API
    YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID')
    YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET')
    YOUTUBE_REDIRECT_URI = os.getenv('YOUTUBE_REDIRECT_URI')
    YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
    
    # Upload settings
    UPLOAD_INTERVAL_HOURS = float(os.getenv('UPLOAD_INTERVAL_HOURS', 2.5))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 262144))
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024 * 1024  # 5GB

class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_ECHO = True

class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_ECHO = False

class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
