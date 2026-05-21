"""
Application entry point.
Run with: python run.py (local development)
For production: gunicorn uses the 'app' object directly
"""
from app import create_app, socketio
import os

app = create_app()

# For production deployment (Render, Heroku, etc.)
# Gunicorn will use this app object
if __name__ == '__main__':
    # Local development mode
    port = int(os.environ.get('PORT', 5001))
    socketio.run(app, debug=True, host='0.0.0.0', port=port,
                 allow_unsafe_werkzeug=True)
