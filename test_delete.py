"""
Test script to verify delete conversation functionality
Run this after trying to delete a conversation to see what's happening
"""
from app import create_app, db
from app.models import Message, User

app = create_app()

with app.app_context():
    # Get admin user
    admin = User.query.filter_by(role='admin').first()
    print(f"\n=== Admin User ===")
    print(f"ID: {admin.id}")
    print(f"Email: {admin.email}")
    
    # Get all applicants
    applicants = User.query.filter_by(role='applicant').all()
    print(f"\n=== Applicants ({len(applicants)}) ===")
    for user in applicants:
        print(f"\nUser ID: {user.id}")
        print(f"Name: {user.name}")
        print(f"Email: {user.email}")
        
        # Count messages
        messages = Message.query.filter(
            db.or_(
                db.and_(Message.sender_id == admin.id, Message.recipient_id == user.id),
                db.and_(Message.sender_id == user.id, Message.recipient_id == admin.id),
            )
        ).all()
        
        print(f"Messages in conversation: {len(messages)}")
        if messages:
            print("Message IDs:", [m.id for m in messages])
