"""
SQLAlchemy Models for AIDP
"""
from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager


# ─────────────────────────────────────────────
#  User model (applicants + admin)
# ─────────────────────────────────────────────
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='applicant')   # 'applicant' | 'admin'
    is_online = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='applicant', lazy=True)
    sent_messages = db.relationship(
        'Message', foreign_keys='Message.sender_id', backref='sender', lazy=True
    )
    received_messages = db.relationship(
        'Message', foreign_keys='Message.recipient_id', backref='recipient', lazy=True
    )

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.email}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ─────────────────────────────────────────────
#  Grant Application model
# ─────────────────────────────────────────────
class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reference_id = db.Column(db.String(20), unique=True, nullable=True)  # Stored reference ID

    # Personal info
    full_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    address = db.Column(db.Text, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    marital_status = db.Column(db.String(30), nullable=False)

    # Financial info
    occupation = db.Column(db.String(150), nullable=False)
    monthly_income = db.Column(db.Numeric(12, 2), nullable=False)
    payment_type = db.Column(db.String(10), nullable=False)   # 'cash' | 'cheque'
    housing_status = db.Column(db.String(10), nullable=False)  # 'own' | 'rent'
    grant_amount = db.Column(db.Numeric(12, 2), nullable=False)  # $100,000–$450,000

    # Application details
    reason = db.Column(db.Text, nullable=False)
    supporting_details = db.Column(db.Text, nullable=True)
    
    # Document upload
    id_document_path = db.Column(db.String(500), nullable=True)  # Path to uploaded ID front
    id_document_back_path = db.Column(db.String(500), nullable=True)  # Path to uploaded ID back

    # Status
    status = db.Column(db.String(20), default='pending')  # pending | approved | rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)

    def get_reference_id(self):
        """Get or generate a human-readable alphanumeric reference ID (8 characters)"""
        if self.reference_id:
            return self.reference_id
        # Generate 8-character alphanumeric ID (uppercase letters and numbers)
        import string
        import random
        # Mix of uppercase letters and numbers for better readability
        alphanumeric = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        self.reference_id = alphanumeric
        # Save to database
        from app import db
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return self.reference_id

    def __repr__(self):
        return f'<Application {self.id} - {self.status}>'


# ─────────────────────────────────────────────
#  Chat Message model
# ─────────────────────────────────────────────
class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)  # Path to uploaded image
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_delivered = db.Column(db.Boolean, default=False)  # One tick
    is_read = db.Column(db.Boolean, default=False)       # Two ticks

    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'sender_name': self.sender.name if self.sender else 'Unknown',
            'sender_role': self.sender.role if self.sender else '',
            'recipient_id': self.recipient_id,
            'body': self.body,
            'image_url': self.image_url,
            'timestamp': self.timestamp.strftime('%I:%M %p'),  # Just time, e.g., "10:30 AM"
            'is_delivered': self.is_delivered,
            'is_read': self.is_read,
        }

    def __repr__(self):
        return f'<Message {self.id} from {self.sender_id}>'


# ─────────────────────────────────────────────
#  Admin Notification model
# ─────────────────────────────────────────────
class AdminNotification(db.Model):
    __tablename__ = 'admin_notifications'

    id = db.Column(db.Integer, primary_key=True)
    notification_type = db.Column(db.String(50), nullable=False)  # 'new_application', 'new_message', etc.
    reference_id = db.Column(db.Integer, nullable=True)  # ID of the related object (application_id, message_id, etc.)
    message = db.Column(db.String(500), nullable=False)  # Notification message
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AdminNotification {self.id} - {self.notification_type}>'
