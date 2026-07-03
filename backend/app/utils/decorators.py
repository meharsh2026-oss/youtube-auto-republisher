"""Utility decorators"""

from functools import wraps
from flask import session, jsonify
from app.models import User

def require_auth(f):
    """Require authentication decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return f(*args, **kwargs)
    
    return decorated_function
