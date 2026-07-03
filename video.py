"""Video and Queue models"""

from app import db
from datetime import datetime

class Video(db.Model):
    """Video model for storing video information"""
    __tablename__ = 'videos'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    youtube_id = db.Column(db.String(255), unique=True, nullable=False)
    title = db.Column(db.String(512))
    description = db.Column(db.Text)
    thumbnail_url = db.Column(db.String(512))
    
    duration_seconds = db.Column(db.Integer)
    local_file_path = db.Column(db.String(512))
    file_size = db.Column(db.Integer)  # in bytes
    
    downloaded_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    queue_items = db.relationship('QueueItem', backref='video', lazy=True, cascade='all, delete-orphan')
    upload_tasks = db.relationship('UploadTask', backref='video', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Video {self.title}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'youtube_id': self.youtube_id,
            'title': self.title,
            'description': self.description,
            'thumbnail_url': self.thumbnail_url,
            'duration_seconds': self.duration_seconds,
            'file_size': self.file_size,
            'downloaded_at': self.downloaded_at.isoformat() if self.downloaded_at else None,
        }

class QueueItem(db.Model):
    """Queue item model for managing upload queue"""
    __tablename__ = 'queue_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), nullable=False)
    
    # Editable metadata
    title = db.Column(db.String(512))
    description = db.Column(db.Text)
    tags = db.Column(db.String(500))  # comma-separated
    
    # Status and settings
    status = db.Column(db.String(50), default='pending')  # pending, downloading, queued, uploading, completed, failed
    privacy = db.Column(db.String(50), default='private')  # private, unlisted, public
    
    # Queue management
    position = db.Column(db.Integer, default=0)
    retry_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    upload_tasks = db.relationship('UploadTask', backref='queue_item', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<QueueItem {self.title} - {self.status}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'video_id': self.video_id,
            'title': self.title,
            'description': self.description,
            'tags': self.tags,
            'status': self.status,
            'privacy': self.privacy,
            'position': self.position,
            'retry_count': self.retry_count,
            'created_at': self.created_at.isoformat(),
        }
