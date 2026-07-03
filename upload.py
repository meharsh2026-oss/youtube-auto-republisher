"""Upload task model"""

from app import db
from datetime import datetime

class UploadTask(db.Model):
    """Upload task model for tracking uploads"""
    __tablename__ = 'upload_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), nullable=False)
    queue_item_id = db.Column(db.Integer, db.ForeignKey('queue_items.id'), nullable=False)
    
    # YouTube video information
    youtube_video_id = db.Column(db.String(255))
    youtube_url = db.Column(db.String(512))
    
    # Upload progress
    status = db.Column(db.String(50), default='pending')  # pending, uploading, completed, failed
    progress_bytes = db.Column(db.Integer, default=0)
    total_bytes = db.Column(db.Integer)
    
    # Error tracking
    error_message = db.Column(db.Text)
    retry_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<UploadTask {self.youtube_video_id} - {self.status}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'video_id': self.video_id,
            'queue_item_id': self.queue_item_id,
            'youtube_video_id': self.youtube_video_id,
            'youtube_url': self.youtube_url,
            'status': self.status,
            'progress_bytes': self.progress_bytes,
            'total_bytes': self.total_bytes,
            'progress_percent': (self.progress_bytes / self.total_bytes * 100) if self.total_bytes else 0,
            'error_message': self.error_message,
            'retry_count': self.retry_count,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }
