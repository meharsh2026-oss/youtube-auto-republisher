"""Routes package"""

from app.routes import auth_bp, videos_bp, queue_bp, upload_bp, settings_bp, logs_bp, health_bp

__all__ = ['auth_bp', 'videos_bp', 'queue_bp', 'upload_bp', 'settings_bp', 'logs_bp', 'health_bp']
