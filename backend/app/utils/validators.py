"""Utility validators"""

import re
from urllib.parse import urlparse

def validate_video_url(url):
    """Validate YouTube video URL"""
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
    return re.match(youtube_regex, url) is not None

def validate_email(email):
    """Validate email address"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    video_id_pattern = r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([A-Za-z0-9_-]{11})'
    match = re.search(video_id_pattern, url)
    return match.group(1) if match else None

def get_file_size_formatted(bytes_size):
    """Format bytes to human readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"
