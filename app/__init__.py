"""
AIDP Application Factory
Initializes Flask app, extensions, and registers blueprints.
"""
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_wtf.csrf import CSRFProtect
from config import Config
from app.email import mail

# --- Extension instances (initialized without app) ---
db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()
csrf = CSRFProtect()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # --- Initialize extensions ---
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(
        app, 
        async_mode='threading',
        cors_allowed_origins='*',
        manage_session=False,
        logger=False,
        engineio_logger=False
    )
    csrf.init_app(app)
    mail.init_app(app)

    # --- Login manager settings ---
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    # --- Register blueprints ---
    from app.routes.auth import auth_bp
    from app.routes.user import user_bp
    from app.routes.admin import admin_bp
    from app.routes.chat import chat_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(chat_bp, url_prefix='/chat')

    # --- Register SocketIO events ---
    from app import sockets  # noqa: F401

    # --- Create DB tables and seed admin ---
    with app.app_context():
        db.create_all()
        _seed_admin(app)

    # --- Context processor: inject `now` into all templates ---
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    # --- Global error handlers ---
    from flask import render_template as rt

    @app.errorhandler(404)
    def not_found(e):
        return rt('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return rt('errors/403.html'), 403

    # --- Root redirect ---
    from flask import redirect, url_for
    from flask_login import current_user

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('user.home'))
        return redirect(url_for('user.home'))

    return app


def _seed_admin(app):
    """Create the default admin account if it does not exist."""
    from app.models import User
    from werkzeug.security import generate_password_hash

    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(
            name=app.config['ADMIN_NAME'],
            email=app.config['ADMIN_EMAIL'],
            password_hash=generate_password_hash(app.config['ADMIN_PASSWORD']),
            role='admin',
        )
        db.session.add(admin)
        db.session.commit()
        print(f"[AIDP] Admin account created: {app.config['ADMIN_EMAIL']}")