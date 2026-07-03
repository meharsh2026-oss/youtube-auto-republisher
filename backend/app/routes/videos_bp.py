"""Video routes"""

from flask import Blueprint, jsonify, session, request, current_app
from app import db
from app.models import User, Video
from app.utils.decorators import require_auth
import os

bp = Blueprint('videos', __name__, url_prefix='/api/videos')

@bp.route('/channels', methods=['GET'])
@require_auth
def get_channels():
    """Get user's YouTube channels"""
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'channel': user.to_dict()
    }), 200

@bp.route('/list', methods=['GET'])
@require_auth
def list_videos():
    """List videos from user's channel"""
    user_id = session.get('user_id')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    videos = Video.query.filter_by(user_id=user_id).paginate(
        page=page, per_page=per_page
    )
    
    return jsonify({
        'videos': [v.to_dict() for v in videos.items],
        'total': videos.total,
        'pages': videos.pages,
        'current_page': page
    }), 200

@bp.route('/search', methods=['POST'])
@require_auth
def search_videos():
    """Search for videos"""
    user_id = session.get('user_id')
    data = request.get_json()
    query = data.get('query', '')
    
    videos = Video.query.filter_by(user_id=user_id).filter(
        Video.title.ilike(f'%{query}%') | Video.description.ilike(f'%{query}%')
    ).all()
    
    return jsonify({
        'videos': [v.to_dict() for v in videos],
        'count': len(videos)
    }), 200

@bp.route('/<int:video_id>', methods=['GET'])
@require_auth
def get_video(video_id):
    """Get video details"""
    video = Video.query.get(video_id)
    
    if not video:
        return jsonify({'error': 'Video not found'}), 404
    
    return jsonify(video.to_dict()), 200

@bp.route('/download', methods=['POST'])
@require_auth
def download_video():
    """Download video"""
    user_id = session.get('user_id')
    data = request.get_json()
    youtube_id = data.get('youtube_id')
    quality = data.get('quality', 'best')
    
    if not youtube_id:
        return jsonify({'error': 'youtube_id is required'}), 400
    
    # Check if video already exists
    video = Video.query.filter_by(youtube_id=youtube_id, user_id=user_id).first()
    if video:
        return jsonify({
            'message': 'Video already exists',
            'video': video.to_dict()
        }), 200
    
    # In production, this would trigger actual download
    # For now, return success
    new_video = Video(
        user_id=user_id,
        youtube_id=youtube_id,
        title='Sample Video',
        description='Sample Description',
        duration_seconds=300
    )
    db.session.add(new_video)
    db.session.commit()
    
    return jsonify({
        'message': 'Download started',
        'video': new_video.to_dict()
    }), 201
