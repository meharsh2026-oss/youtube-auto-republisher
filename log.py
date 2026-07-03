"""Application log model"""

from app import db
from datetime import datetime

class AppLog(db.Model):
    """Application log model for tracking operations"""
    __tablename__ = 'app_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Log information
    level = db.Column(db.String(50))  # INFO, WARNING, ERROR, DEBUG
    message = db.Column(db.Text)
    source = db.Column(db.String(255))  # auth, videos, upload, queue, etc.
    
    # Additional context
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), nullable=True)
    queue_item_id = db.Column(db.Integer, db.ForeignKey('queue_items.id'), nullable=True)
    upload_task_id = db.Column(db.Integer, db.ForeignKey('upload_tasks.id'), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AppLog {self.level} - {self.message[:50]}'>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'level': self.level,
            'message': self.message,
            'source': self.source,
            'created_at': self.created_at.isoformat(),
        }
