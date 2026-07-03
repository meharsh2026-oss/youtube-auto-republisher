"""Settings routes"""

from flask import Blueprint, jsonify, session, request
from app import db
from app.models import User, Settings
from app.utils.decorators import require_auth

bp = Blueprint('settings', __name__, url_prefix='/api/settings')

@bp.route('', methods=['GET'])
@require_auth
def get_settings():
    """Get user settings"""
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user or not user.settings:
        return jsonify({'error': 'Settings not found'}), 404
    
    return jsonify(user.settings.to_dict()), 200

@bp.route('', methods=['PUT'])
@require_auth
def update_settings():
    """Update user settings"""
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user or not user.settings:
        return jsonify({'error': 'Settings not found'}), 404
    
    data = request.get_json()
    settings = user.settings
    
    if 'auto_upload_enabled' in data:
        settings.auto_upload_enabled = data['auto_upload_enabled']
    if 'upload_interval_hours' in data:
        settings.upload_interval_hours = data['upload_interval_hours']
    if 'daily_upload_limit' in data:
        settings.daily_upload_limit = data['daily_upload_limit']
    if 'default_privacy' in data:
        settings.default_privacy = data['default_privacy']
    if 'default_video_quality' in data:
        settings.default_video_quality = data['default_video_quality']
    if 'notify_on_upload' in data:
        settings.notify_on_upload = data['notify_on_upload']
    if 'notify_on_error' in data:
        settings.notify_on_error = data['notify_on_error']
    
    db.session.commit()
    
    return jsonify(settings.to_dict()), 200
