"""Upload routes"""

from flask import Blueprint, jsonify, session, request
from app import db
from app.models import User, UploadTask, QueueItem
from app.utils.decorators import require_auth

bp = Blueprint('upload', __name__, url_prefix='/api/upload')

@bp.route('/start', methods=['POST'])
@require_auth
def start_upload():
    """Start video upload"""
    user_id = session.get('user_id')
    data = request.get_json()
    queue_item_id = data.get('queue_item_id')
    
    if not queue_item_id:
        return jsonify({'error': 'queue_item_id is required'}), 400
    
    queue_item = QueueItem.query.get(queue_item_id)
    if not queue_item or queue_item.user_id != user_id:
        return jsonify({'error': 'Queue item not found'}), 404
    
    upload_task = UploadTask(
        user_id=user_id,
        video_id=queue_item.video_id,
        queue_item_id=queue_item_id,
        status='pending'
    )
    db.session.add(upload_task)
    queue_item.status = 'uploading'
    db.session.commit()
    
    return jsonify(upload_task.to_dict()), 201

@bp.route('/<int:task_id>/progress', methods=['GET'])
@require_auth
def get_upload_progress(task_id):
    """Get upload progress"""
    user_id = session.get('user_id')
    upload_task = UploadTask.query.get(task_id)
    
    if not upload_task or upload_task.user_id != user_id:
        return jsonify({'error': 'Upload task not found'}), 404
    
    return jsonify(upload_task.to_dict()), 200

@bp.route('/<int:task_id>/retry', methods=['POST'])
@require_auth
def retry_upload(task_id):
    """Retry failed upload"""
    user_id = session.get('user_id')
    upload_task = UploadTask.query.get(task_id)
    
    if not upload_task or upload_task.user_id != user_id:
        return jsonify({'error': 'Upload task not found'}), 404
    
    if upload_task.status != 'failed':
        return jsonify({'error': 'Upload is not in failed status'}), 400
    
    upload_task.status = 'pending'
    upload_task.retry_count += 1
    upload_task.error_message = None
    db.session.commit()
    
    return jsonify(upload_task.to_dict()), 200
