"""YouTube API service"""

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import logging

logger = logging.getLogger(__name__)

class YouTubeService:
    """Service for YouTube API operations"""
    
    def __init__(self, credentials):
        """Initialize with user credentials"""
        self.credentials = credentials
        self.youtube = build('youtube', 'v3', credentials=credentials)
    
    def get_channels(self):
        """Get user's channels"""
        try:
            response = self.youtube.channels().list(
                part='snippet,statistics',
                mine=True
            ).execute()
            return response.get('items', [])
        except Exception as e:
            logger.error(f'Error getting channels: {str(e)}')
            return []
    
    def upload_video(self, file_path, metadata):
        """Upload video to YouTube"""
        try:
            request = self.youtube.videos().insert(
                part='snippet,status',
                body={
                    'snippet': {
                        'title': metadata.get('title'),
                        'description': metadata.get('description'),
                        'tags': metadata.get('tags', []),
                        'categoryId': '22'  # People & Blogs
                    },
                    'status': {
                        'privacyStatus': metadata.get('privacy', 'private')
                    }
                },
                media_body=file_path
            )
            
            response = request.execute()
            logger.info(f'Video uploaded: {response["id"]}')
            return response
        except Exception as e:
            logger.error(f'Error uploading video: {str(e)}')
            raise
