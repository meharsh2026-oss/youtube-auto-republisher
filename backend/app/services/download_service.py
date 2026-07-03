"""Video download service"""

import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class DownloadService:
    """Service for downloading videos"""
    
    def __init__(self, download_folder='./downloads'):
        """Initialize download service"""
        self.download_folder = download_folder
        Path(download_folder).mkdir(parents=True, exist_ok=True)
    
    def download_video(self, youtube_url, quality='best'):
        """Download video from YouTube"""
        try:
            import yt_dlp
            
            ydl_opts = {
                'format': f'best[height<={quality.replace("p", "")}]/best',
                'outtmpl': os.path.join(self.download_folder, '%(title)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=True)
                logger.info(f'Downloaded: {info["title"]}')
                return info
        except Exception as e:
            logger.error(f'Error downloading video: {str(e)}')
            raise
    
    def get_video_info(self, youtube_url):
        """Get video information without downloading"""
        try:
            import yt_dlp
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=False)
                return info
        except Exception as e:
            logger.error(f'Error getting video info: {str(e)}')
            raise
