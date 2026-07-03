"""Authentication routes"""

from flask import Blueprint, jsonify, session, redirect, request, current_app
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from app import db
from app.models import User, Settings
import google.auth.transport.requests
import os

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login', methods=['GET'])
def login():
    """Start OAuth flow"""
    flow = Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=current_app.config['YOUTUBE_SCOPES'],
        redirect_uri=current_app.config['YOUTUBE_REDIRECT_URI']
    )
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    
    session['state'] = state
    return redirect(authorization_url)

@bp.route('/callback', methods=['GET'])
def callback():
    """OAuth callback"""
    state = session.get('state')
    code = request.args.get('code')
    
    if not state or not code:
        return jsonify({'error': 'Missing state or code'}), 400
    
    flow = Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=current_app.config['YOUTUBE_SCOPES'],
        state=state,
        redirect_uri=current_app.config['YOUTUBE_REDIRECT_URI']
    )
    
    flow.fetch_token(code=code)
    credentials = flow.credentials
    
    # Get user info from YouTube
    from googleapiclient.discovery import build
    youtube = build('youtube', 'v3', credentials=credentials)
    
    channels = youtube.channels().list(
        part='snippet',
        mine=True
    ).execute()
    
    if not channels['items']:
        return jsonify({'error': 'No YouTube channel found'}), 400
    
    channel = channels['items'][0]
    channel_id = channel['id']
    channel_title = channel['snippet']['title']
    channel_thumbnail = channel['snippet']['thumbnails'].get('high', {}).get('url')
    
    # Create or update user
    user = User.query.filter_by(channel_id=channel_id).first()
    if not user:
        user = User(
            username=channel_title,
            channel_id=channel_id,
            channel_title=channel_title,
            channel_thumbnail=channel_thumbnail,
        )
        db.session.add(user)
    else:
        user.channel_title = channel_title
        user.channel_thumbnail = channel_thumbnail
    
    user.access_token = credentials.token
    user.refresh_token = credentials.refresh_token
    user.token_expiry = credentials.expiry
    
    db.session.commit()
    
    # Create default settings if not exists
    if not user.settings:
        settings = Settings(user_id=user.id)
        db.session.add(settings)
        db.session.commit()
    
    session['user_id'] = user.id
    
    return redirect('/')

@bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@bp.route('/status', methods=['GET'])
def auth_status():
    """Check authentication status"""
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'authenticated': False}), 200
    
    user = User.query.get(user_id)
    if not user:
        session.clear()
        return jsonify({'authenticated': False}), 200
    
    return jsonify({
        'authenticated': True,
        'user': user.to_dict()
    }), 200
