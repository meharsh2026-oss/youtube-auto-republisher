"""Settings model"""

from app import db
from datetime import datetime

class Settings(db.Model):
    """Settings model for user preferences"""
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Upload settings
    auto_upload_enabled = db.Column(db.Boolean, default=True)
    upload_interval_hours = db.Column(db.Float, default=2.5)
    daily_upload_limit = db.Column(db.Integer, default=10)
    
    # Video settings
    default_privacy = db.Column(db.String(50), default='private')
    default_video_quality = db.Column(db.String(50), default='best')
    add_watermark = db.Column(db.Boolean, default=False)
    
    # Notification settings
    notify_on_upload = db.Column(db.Boolean, default=True)
    notify_on_error = db.Column(db.Boolean, default=True)
    
    # Advanced settings
    max_retries = db.Column(db.Integer, default=3)
    chunk_size = db.Column(db.Integer, default=262144)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Settings user_id={self.user_id}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'auto_upload_enabled': self.auto_upload_enabled,
            'upload_interval_hours': self.upload_interval_hours,
            'daily_upload_limit': self.daily_upload_limit,
            'default_privacy': self.default_privacy,
            'default_video_quality': self.default_video_quality,
            'add_watermark': self.add_watermark,
            'notify_on_upload': self.notify_on_upload,
            'notify_on_error': self.notify_on_error,
            'max_retries': self.max_retries,
        }
