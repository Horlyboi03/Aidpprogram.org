import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'aidp-super-secret-key-change-in-production')
    WTF_CSRF_ENABLED = True

    # Database
    database_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/aidp_db')
    # Fix for Render/Heroku postgres:// to postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SocketIO
    SOCKETIO_ASYNC_MODE = 'threading'

    # Admin credentials (set via environment in production)
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@aidp.org')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Admin@1234')
    ADMIN_NAME = os.environ.get('ADMIN_NAME', 'AIDP Administrator')

    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'your-email@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'your-app-password')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', os.environ.get('MAIL_USERNAME', 'noreply@aidp.org'))

    # File Upload Configuration
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'app/static/uploads')
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf'}
