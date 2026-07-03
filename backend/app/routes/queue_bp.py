"""Queue routes"""

from flask import Blueprint, jsonify, session, request
from app import db
from app.models import User, QueueItem, Video
from app.utils.decorators import require_auth

bp = Blueprint('queue', __name__, url_prefix='/api/queue')

@bp.route('', methods=['GET'])
@require_auth
def get_queue():
    """Get user's queue"""
    user_id = session.get('user_id')
    
    queue_items = QueueItem.query.filter_by(user_id=user_id).order_by(QueueItem.position).all()
    
    return jsonify({
        'queue': [item.to_dict() for item in queue_items],
        'count': len(queue_items)
    }), 200

@bp.route('', methods=['POST'])
@require_auth
def add_to_queue():
    """Add video to queue"""
    user_id = session.get('user_id')
    data = request.get_json()
    video_id = data.get('video_id')
    
    if not video_id:
        return jsonify({'error': 'video_id is required'}), 400
    
    video = Video.query.get(video_id)
    if not video or video.user_id != user_id:
        return jsonify({'error': 'Video not found'}), 404
    
    # Check if already in queue
    existing = QueueItem.query.filter_by(video_id=video_id, user_id=user_id).first()
    if existing:
        return jsonify({'error': 'Video already in queue'}), 400
    
    # Get next position
    last_position = db.session.query(db.func.max(QueueItem.position)).filter_by(user_id=user_id).scalar() or 0
    
    queue_item = QueueItem(
        user_id=user_id,
        video_id=video_id,
        title=video.title,
        description=video.description,
        position=last_position + 1
    )
    db.session.add(queue_item)
    db.session.commit()
    
    return jsonify(queue_item.to_dict()), 201

@bp.route('/<int:item_id>', methods=['PUT'])
@require_auth
def update_queue_item(item_id):
    """Update queue item"""
    user_id = session.get('user_id')
    queue_item = QueueItem.query.get(item_id)
    
    if not queue_item or queue_item.user_id != user_id:
        return jsonify({'error': 'Queue item not found'}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        queue_item.title = data['title']
    if 'description' in data:
        queue_item.description = data['description']
    if 'tags' in data:
        queue_item.tags = data['tags']
    if 'privacy' in data:
        queue_item.privacy = data['privacy']
    if 'position' in data:
        queue_item.position = data['position']
    
    db.session.commit()
    
    return jsonify(queue_item.to_dict()), 200

@bp.route('/<int:item_id>', methods=['DELETE'])
@require_auth
def remove_from_queue(item_id):
    """Remove from queue"""
    user_id = session.get('user_id')
    queue_item = QueueItem.query.get(item_id)
    
    if not queue_item or queue_item.user_id != user_id:
        return jsonify({'error': 'Queue item not found'}), 404
    
    db.session.delete(queue_item)
    db.session.commit()
    
    return jsonify({'message': 'Removed from queue'}), 200
