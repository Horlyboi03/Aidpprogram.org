"""
Migration script to add admin_notifications table
Run this once: python add_admin_notifications_table.py
"""
from app import create_app, db
from app.models import AdminNotification

app = create_app()

with app.app_context():
    print("Creating admin_notifications table...")
    db.create_all()
    print("✓ admin_notifications table created successfully!")
    print("\nYou can now track admin notifications for new applications.")
