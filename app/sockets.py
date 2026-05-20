"""
Flask-SocketIO event handlers for real-time chat.
All events run in the application context.
"""
import os
import base64
from pathlib import Path
from datetime import datetime
from flask import request
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from app import socketio, db
from app.models import Message, User


@socketio.on('connect')
def handle_connect():
    """Mark user as online when they connect."""
    if current_user.is_authenticated:
        current_user.is_online = True
        db.session.commit()
        # Join a personal room named after user id
        join_room(f'user_{current_user.id}')
        emit('status', {'user_id': current_user.id, 'online': True}, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    """Mark user as offline on disconnect."""
    if current_user.is_authenticated:
        current_user.is_online = False
        db.session.commit()
        emit('status', {'user_id': current_user.id, 'online': False}, broadcast=True)


@socketio.on('send_message')
def handle_send_message(data):
    """
    Expected data:
      {
        'recipient_id': int,
        'body': str
      }
    """
    print(f"[SOCKET] send_message received: {data}")
    
    if not current_user.is_authenticated:
        print("[SOCKET] User not authenticated")
        return

    recipient_id = data.get('recipient_id')
    body = data.get('body', '').strip()

    if not body or not recipient_id:
        print(f"[SOCKET] Missing body or recipient_id: body={body}, recipient_id={recipient_id}")
        return

    recipient = User.query.get(recipient_id)
    if not recipient:
        print(f"[SOCKET] Recipient not found: {recipient_id}")
        return

    # Persist message
    msg = Message(
        sender_id=current_user.id,
        recipient_id=recipient_id,
        body=body,
        is_delivered=True,  # Always mark as delivered immediately
    )
    db.session.add(msg)
    db.session.commit()
    
    print(f"[SOCKET] Message saved: ID={msg.id}, From={msg.sender_id}, To={msg.recipient_id}")

    payload = msg.to_dict()
    print(f"[SOCKET] Emitting to rooms: user_{current_user.id}, user_{recipient_id}")

    # Emit to sender's own room (so multiple tabs stay in sync)
    emit('receive_message', payload, room=f'user_{current_user.id}')
    # Emit to recipient's room
    emit('receive_message', payload, room=f'user_{recipient_id}')
    
    # If recipient is online, they'll mark it as read automatically
    # Otherwise it stays as delivered (one tick)


@socketio.on('send_image')
def handle_send_image(data):
    """
    Handle image upload via Socket.IO.
    Expected data:
      {
        'recipient_id': int,
        'image_data': str (base64),
        'image_name': str,
        'image_type': str
      }
    """
    print(f"[SOCKET] send_image received from user {current_user.id}")
    
    if not current_user.is_authenticated:
        print("[SOCKET] User not authenticated")
        return

    recipient_id = data.get('recipient_id')
    image_data = data.get('image_data')
    image_name = data.get('image_name', 'image.jpg')
    image_type = data.get('image_type', 'image/jpeg')

    if not image_data or not recipient_id:
        print(f"[SOCKET] Missing image_data or recipient_id")
        return

    recipient = User.query.get(recipient_id)
    if not recipient:
        print(f"[SOCKET] Recipient not found: {recipient_id}")
        return

    try:
        # Decode base64 image
        image_data = image_data.split(',')[1] if ',' in image_data else image_data
        image_bytes = base64.b64decode(image_data)
        
        # Create uploads directory if it doesn't exist
        uploads_dir = Path('app/static/uploads/chat')
        uploads_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.utcnow().timestamp()
        ext = image_name.split('.')[-1] if '.' in image_name else 'jpg'
        filename = f"{current_user.id}_{timestamp}.{ext}"
        file_path = uploads_dir / filename
        
        # Save image
        with open(file_path, 'wb') as f:
            f.write(image_bytes)
        
        # Store relative path for URL
        image_url = f"uploads/chat/{filename}"
        
        # Persist message with image
        msg = Message(
            sender_id=current_user.id,
            recipient_id=recipient_id,
            body='[Image]',  # Placeholder text
            image_url=image_url,
            is_delivered=True,
        )
        db.session.add(msg)
        db.session.commit()
        
        print(f"[SOCKET] Image message saved: ID={msg.id}, URL={image_url}")

        payload = msg.to_dict()
        print(f"[SOCKET] Emitting image to rooms: user_{current_user.id}, user_{recipient_id}")

        # Emit to sender's own room
        emit('receive_message', payload, room=f'user_{current_user.id}')
        # Emit to recipient's room
        emit('receive_message', payload, room=f'user_{recipient_id}')
        
    except Exception as e:
        print(f"[SOCKET] Error saving image: {e}")
        return


@socketio.on('message_delivered')
def handle_message_delivered(data):
    """
    Mark message as delivered when recipient receives it.
    Expected data: { 'message_id': int }
    """
    if not current_user.is_authenticated:
        return
    
    message_id = data.get('message_id')
    if not message_id:
        return
    
    msg = Message.query.get(message_id)
    if msg and msg.recipient_id == current_user.id and not msg.is_delivered:
        msg.is_delivered = True
        db.session.commit()
        
        # Notify sender about delivery
        emit('message_status_update', {
            'message_id': msg.id,
            'is_delivered': True,
            'is_read': msg.is_read
        }, room=f'user_{msg.sender_id}')


@socketio.on('message_read')
def handle_message_read(data):
    """
    Mark message as read when recipient views it.
    Expected data: { 'message_id': int }
    """
    if not current_user.is_authenticated:
        return
    
    message_id = data.get('message_id')
    if not message_id:
        return
    
    msg = Message.query.get(message_id)
    if msg and msg.recipient_id == current_user.id and not msg.is_read:
        msg.is_delivered = True  # Ensure delivered is also true
        msg.is_read = True
        db.session.commit()
        
        # Notify sender about read status
        emit('message_status_update', {
            'message_id': msg.id,
            'is_delivered': True,
            'is_read': True
        }, room=f'user_{msg.sender_id}')


@socketio.on('mark_conversation_read')
def handle_mark_conversation_read(data):
    """
    Mark all messages in a conversation as read.
    Expected data: { 'sender_id': int }
    """
    if not current_user.is_authenticated:
        return
    
    sender_id = data.get('sender_id')
    if not sender_id:
        return
    
    # Mark all unread messages from this sender as read
    messages = Message.query.filter_by(
        sender_id=sender_id,
        recipient_id=current_user.id,
        is_read=False
    ).all()
    
    for msg in messages:
        msg.is_delivered = True
        msg.is_read = True
    
    db.session.commit()
    
    # Notify sender about read status for all messages
    for msg in messages:
        emit('message_status_update', {
            'message_id': msg.id,
            'is_delivered': True,
            'is_read': True
        }, room=f'user_{sender_id}')

