"""User model"""

from app import db
from datetime import datetime

class User(db.Model):
    """User model for storing YouTube channel information"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    channel_id = db.Column(db.String(255), unique=True, nullable=False)
    channel_title = db.Column(db.String(255))
    channel_thumbnail = db.Column(db.String(512))
    
    # OAuth tokens
    access_token = db.Column(db.Text)
    refresh_token = db.Column(db.Text)
    token_expiry = db.Column(db.DateTime)
    
    # User preferences
    upload_interval = db.Column(db.Float, default=2.5)
    default_privacy = db.Column(db.String(50), default='private')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    videos = db.relationship('Video', backref='user', lazy=True, cascade='all, delete-orphan')
    queue_items = db.relationship('QueueItem', backref='user', lazy=True, cascade='all, delete-orphan')
    upload_tasks = db.relationship('UploadTask', backref='user', lazy=True, cascade='all, delete-orphan')
    settings = db.relationship('Settings', backref='user', uselist=False, cascade='all, delete-orphan')
    logs = db.relationship('AppLog', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.channel_title}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'channel_id': self.channel_id,
            'channel_title': self.channel_title,
            'channel_thumbnail': self.channel_thumbnail,
            'default_privacy': self.default_privacy,
            'upload_interval': self.upload_interval,
            'created_at': self.created_at.isoformat(),
        }
