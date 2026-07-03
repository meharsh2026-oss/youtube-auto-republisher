"""Logs routes"""

from flask import Blueprint, jsonify, session, request
from app import db
from app.models import AppLog
from app.utils.decorators import require_auth

bp = Blueprint('logs', __name__, url_prefix='/api/logs')

@bp.route('', methods=['GET'])
@require_auth
def get_logs():
    """Get application logs"""
    user_id = session.get('user_id')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    level = request.args.get('level', None)
    
    query = AppLog.query.filter_by(user_id=user_id)
    
    if level:
        query = query.filter_by(level=level)
    
    logs = query.order_by(AppLog.created_at.desc()).paginate(
        page=page, per_page=per_page
    )
    
    return jsonify({
        'logs': [log.to_dict() for log in logs.items],
        'total': logs.total,
        'pages': logs.pages,
        'current_page': page
    }), 200

@bp.route('/clear', methods=['POST'])
@require_auth
def clear_logs():
    """Clear old logs"""
    user_id = session.get('user_id')
    days = request.get_json().get('days', 30)
    
    from datetime import datetime, timedelta
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    AppLog.query.filter_by(user_id=user_id).filter(
        AppLog.created_at < cutoff_date
    ).delete()
    
    db.session.commit()
    
    return jsonify({'message': f'Cleared logs older than {days} days'}), 200
