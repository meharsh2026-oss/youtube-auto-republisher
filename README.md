# YouTube Auto Republisher

## 🎬 Automatically republish your YouTube videos on schedule

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](#)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## ✨ Features

✅ **OAuth 2.0 Authentication** - Secure YouTube connection  
✅ **Automatic Scheduling** - Upload every 2.5 hours (customizable)  
✅ **Queue Management** - Organize and edit video metadata  
✅ **High-Quality Downloads** - Preserve original video quality  
✅ **Progress Tracking** - Real-time upload status  
✅ **Automatic Retries** - Smart retry logic for failures  
✅ **Comprehensive Logging** - Track all operations  
✅ **Beautiful UI** - Dark theme, responsive design  
✅ **Production Ready** - Error handling, validation, security  
✅ **Multi-Platform Deploy** - Docker, Railway, Render, VPS  

## 🛠 Tech Stack

### Backend
- **Python 3.8+** - Programming language
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database
- **Google API Client** - YouTube integration
- **yt-dlp** - Video downloading
- **APScheduler** - Task scheduling
- **Gunicorn** - Production server

### Frontend
- **HTML5** - Structure
- **Tailwind CSS** - Styling
- **Vanilla JavaScript** - No dependencies
- **Font Awesome** - Icons

### Database
- **SQLite** - Development/small deployments
- **PostgreSQL** - Production/large deployments

### Deployment
- **Docker** - Containerization
- **Railway** - Cloud platform
- **Render** - Cloud platform
- **VPS** - Self-hosted

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- FFmpeg
- YouTube API credentials
- Git

### Installation

```bash
# Clone repository
git clone https://github.com/meharsh2026-oss/youtube-auto-republisher.git
cd youtube-auto-republisher/backend

# Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with YouTube API credentials

# Initialize database
flask db upgrade

# Run application
flask run
```

### Access Application

Open http://localhost:5000 in your browser

## 📁 Project Structure

```
youtube-auto-republisher/
├── backend/
│   ├── app/
│   │   ├── __init__.py           # App factory
│   │   ├── config.py              # Configuration
│   │   ├── models/                # Database models
│   │   │   ├── user.py
│   │   │   ├── video.py
│   │   │   ├── upload.py
│   │   │   ├── settings.py
│   │   │   └── log.py
│   │   ├── routes/                # API endpoints
│   │   │   ├── auth_bp.py
│   │   │   ├── videos_bp.py
│   │   │   ├── queue_bp.py
│   │   │   ├── upload_bp.py
│   │   │   ├── settings_bp.py
│   │   │   ├── logs_bp.py
│   │   │   └── health_bp.py
│   │   ├── services/              # Business logic
│   │   │   ├── youtube_service.py
│   │   │   ├── download_service.py
│   │   │   ├── upload_service.py
│   │   │   └── scheduler_service.py
│   │   └── utils/
│   │       ├── decorators.py
│   │       └── validators.py
│   ├── run.py                     # Entry point
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
├── frontend/
│   ├── index.html                 # Main page
│   ├── css/style.css              # Styling
│   └── js/app.js                  # Frontend logic
├── README.md
├── INSTALLATION.md
├── DEPLOYMENT.md
├── LICENSE
├── Dockerfile
└── docker-compose.yml
```

## 🔌 API Documentation

### Authentication

```
GET    /api/auth/login              Start OAuth flow
GET    /api/auth/callback           OAuth callback
POST   /api/auth/logout             Logout
GET    /api/auth/status             Check auth status
```

### Videos

```
GET    /api/videos/channels         List channels
GET    /api/videos/list             List videos
POST   /api/videos/search           Search videos
GET    /api/videos/<id>             Get video details
POST   /api/videos/download         Download video
```

### Queue

```
GET    /api/queue                   Get queue
POST   /api/queue                   Add to queue
PUT    /api/queue/<id>              Update queue item
DELETE /api/queue/<id>              Remove from queue
```

### Upload

```
POST   /api/upload/start            Start upload
GET    /api/upload/<id>/progress    Get progress
POST   /api/upload/<id>/retry       Retry upload
```

### Settings

```
GET    /api/settings                Get settings
PUT    /api/settings                Update settings
```

### Logs

```
GET    /api/logs                    Get logs
POST   /api/logs/clear              Clear old logs
```

### Health

```
GET    /api/health                  Health check
```

## ⚙️ Configuration

### Environment Variables

```env
# Flask
FLASK_ENV=development|production
FLASK_SECRET_KEY=your-secret-key

# YouTube API
YOUTUBE_CLIENT_ID=xxx.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=xxx
YOUTUBE_REDIRECT_URI=http://localhost:5000/api/auth/callback

# Database
DATABASE_URL=sqlite:///app.db

# Folders
DOWNLOAD_FOLDER=./downloads
TEMP_FOLDER=./temp
LOGS_FOLDER=./logs

# Upload
UPLOAD_INTERVAL_HOURS=2.5
MAX_RETRIES=3
CHUNK_SIZE=262144

# Logging
LOG_LEVEL=INFO
```

## 🚀 Deployment

### Docker

```bash
docker-compose up -d
```

### Railway

1. Connect GitHub repo
2. Set environment variables
3. Deploy!

### Render

1. Create Web Service
2. Connect GitHub
3. Set build/start commands
4. Deploy!

### VPS

See DEPLOYMENT.md for detailed VPS setup.

## 🆘 Troubleshooting

### Port Already in Use

```bash
flask run --port 5001
```

### Module Not Found

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### FFmpeg Not Found

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
```bash
choco install ffmpeg
```

For more troubleshooting, see INSTALLATION.md

## 📚 Documentation

- **README.md** - This file (overview)
- **SETUP.md** - Quick setup reference
- **INSTALLATION.md** - Detailed installation
- **DEPLOYMENT.md** - Deployment options
- **PROJECT_OVERVIEW.md** - Architecture details
- **WALKTHROUGH.md** - Step-by-step guide

## 🔐 Security

⚠️ **IMPORTANT**: This application is designed **ONLY** for videos you own or have permission to reuse.

- Respect YouTube's Terms of Service
- Respect copyright laws
- Obtain proper licenses for reuse
- YouTube may disable accounts for violations

### Security Features

✅ OAuth 2.0 authentication
✅ Secure token storage
✅ Environment variables for secrets
✅ Input validation
✅ SQL injection prevention
✅ CSRF protection
✅ HTTPS support

## 📊 Database Models

### User
- YouTube channel information
- OAuth tokens
- User preferences

### Video
- Video metadata
- Download information
- Local file path

### QueueItem
- Queued videos
- Metadata editing
- Priority/position

### UploadTask
- Upload tracking
- Progress information
- Retry count

### Settings
- User preferences
- Upload schedule
- Quality settings

### AppLog
- Operation logs
- Error tracking
- Audit trail

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## 📄 License

MIT License - See LICENSE file

## 🙏 Support

- 📖 Read documentation
- 🐛 Check GitHub issues
- 💬 Ask on Stack Overflow
- 📧 Contact developer

## 🎯 Roadmap

- [ ] Batch upload scheduling
- [ ] Video analytics integration
- [ ] Multiple channel support
- [ ] Advanced metadata templates
- [ ] Webhook support
- [ ] Mobile app
- [ ] API rate limiting
- [ ] Advanced scheduling (cron)

## 👨‍💻 Author

**Harsh Mehta** - [@meharsh2026-oss](https://github.com/meharsh2026-oss)

## 🎉 Acknowledgments

- YouTube Data API v3 documentation
- yt-dlp for video downloading
- Flask and SQLAlchemy communities
- Tailwind CSS for styling

---

**Happy republishing!** 🚀

Made with ❤️ for content creators
