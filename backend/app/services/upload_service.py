"""Video upload service"""

import logging

logger = logging.getLogger(__name__)

class UploadService:
    """Service for uploading videos"""
    
    def __init__(self, youtube_service):
        """Initialize upload service"""
        self.youtube_service = youtube_service
    
    def upload_video(self, file_path, metadata):
        """Upload video to YouTube"""
        try:
            result = self.youtube_service.upload_video(file_path, metadata)
            logger.info(f'Video uploaded successfully: {result["id"]}')
            return result
        except Exception as e:
            logger.error(f'Upload failed: {str(e)}')
            raise
    
    def update_video(self, video_id, metadata):
        """Update video metadata"""
        try:
            # Implementation for updating video metadata
            logger.info(f'Video updated: {video_id}')
        except Exception as e:
            logger.error(f'Error updating video: {str(e)}')
            raise
