"""Health check route"""

from flask import Blueprint, jsonify
from app import db

bp = Blueprint('health', __name__, url_prefix='/api/health')

@bp.route('', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 500
