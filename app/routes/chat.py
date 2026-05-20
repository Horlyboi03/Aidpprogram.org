"""
Chat HTTP routes (history endpoint) — SocketIO events in sockets.py
"""
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Message, User

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/history/<int:other_user_id>')
@login_required
def history(other_user_id):
    """Return JSON chat history between current_user and other_user_id."""
    other_user = User.query.get_or_404(other_user_id)
    messages = Message.query.filter(
        db.or_(
            db.and_(Message.sender_id == current_user.id, Message.recipient_id == other_user_id),
            db.and_(Message.sender_id == other_user_id, Message.recipient_id == current_user.id),
        )
    ).order_by(Message.timestamp.asc()).all()

    return jsonify([m.to_dict() for m in messages])
