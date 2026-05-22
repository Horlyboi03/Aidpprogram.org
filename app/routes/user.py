"""
User-facing routes: home, dashboard, apply, chat
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Application, Message, User, AdminNotification
from app.email import send_application_confirmation, send_application_approved, send_application_rejected
from decimal import Decimal
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from pathlib import Path

user_bp = Blueprint('user', __name__)


@user_bp.context_processor
def inject_user_notifications():
    """Inject notification counts into all user templates."""
    if current_user.is_authenticated and not current_user.is_admin():
        # Count unread messages from admin
        admin = User.query.filter_by(role='admin').first()
        unread_messages = 0
        if admin:
            unread_messages = Message.query.filter_by(
                sender_id=admin.id,
                recipient_id=current_user.id,
                is_read=False
            ).count()
        
        return {'user_notifications': {'unread_messages': unread_messages}}
    return {'user_notifications': {'unread_messages': 0}}


@user_bp.route('/home')
def home():
    # Allow anyone to view the home page (no redirect for admins)
    return render_template('user/home.html')


@user_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))

    application = Application.query.filter_by(user_id=current_user.id).first()
    # Get unread messages count
    admin = User.query.filter_by(role='admin').first()
    unread = 0
    if admin:
        unread = Message.query.filter_by(
            sender_id=admin.id,
            recipient_id=current_user.id,
            is_read=False
        ).count()

    return render_template('user/dashboard.html', application=application, unread=unread)


@user_bp.route('/apply', methods=['GET', 'POST'])
@login_required
def apply():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))

    # One application per user
    existing = Application.query.filter_by(user_id=current_user.id).first()
    if existing:
        flash('You have already submitted an application.', 'info')
        return redirect(url_for('user.dashboard'))

    if request.method == 'POST':
        try:
            grant_amount = Decimal(request.form.get('grant_amount_requested', '0'))
            if not (100000 <= grant_amount <= 450000):
                flash('Grant amount must be between $100,000 and $450,000.', 'danger')
                return render_template('user/apply.html', form_data=request.form)

            dob = datetime.strptime(request.form.get('date_of_birth', ''), '%Y-%m-%d').date()

            # Handle file uploads (front and back)
            id_document_path = None
            id_document_back_path = None
            
            # Front ID upload
            if 'id_document' in request.files:
                file = request.files['id_document']
                if file and file.filename != '':
                    # Validate file
                    allowed_extensions = {'jpg', 'jpeg', 'png', 'pdf'}
                    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                        flash('Invalid file type for front ID. Please upload JPG, PNG, or PDF.', 'danger')
                        return render_template('user/apply.html', form_data=request.form)
                    
                    # Check file size (5MB max)
                    file.seek(0, os.SEEK_END)
                    file_size = file.tell()
                    file.seek(0)
                    if file_size > 5 * 1024 * 1024:
                        flash('Front ID file size must be less than 5MB.', 'danger')
                        return render_template('user/apply.html', form_data=request.form)
                    
                    # Create uploads directory if it doesn't exist
                    uploads_dir = Path('app/static/uploads/documents')
                    uploads_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Save file with secure name
                    filename = secure_filename(f"{current_user.id}_{datetime.utcnow().timestamp()}_front_{file.filename}")
                    file_path = uploads_dir / filename
                    file.save(str(file_path))
                    id_document_path = f"uploads/documents/{filename}"
            
            # Back ID upload
            if 'id_document_back' in request.files:
                file = request.files['id_document_back']
                if file and file.filename != '':
                    # Validate file
                    allowed_extensions = {'jpg', 'jpeg', 'png', 'pdf'}
                    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
                        flash('Invalid file type for back ID. Please upload JPG, PNG, or PDF.', 'danger')
                        return render_template('user/apply.html', form_data=request.form)
                    
                    # Check file size (5MB max)
                    file.seek(0, os.SEEK_END)
                    file_size = file.tell()
                    file.seek(0)
                    if file_size > 5 * 1024 * 1024:
                        flash('Back ID file size must be less than 5MB.', 'danger')
                        return render_template('user/apply.html', form_data=request.form)
                    
                    # Create uploads directory if it doesn't exist
                    uploads_dir = Path('app/static/uploads/documents')
                    uploads_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Save file with secure name
                    filename = secure_filename(f"{current_user.id}_{datetime.utcnow().timestamp()}_back_{file.filename}")
                    file_path = uploads_dir / filename
                    file.save(str(file_path))
                    id_document_back_path = f"uploads/documents/{filename}"

            app_obj = Application(
                user_id=current_user.id,
                full_name=request.form.get('full_name', '').strip(),
                email=request.form.get('email', '').strip().lower(),
                phone=request.form.get('phone', '').strip(),
                address=request.form.get('address', '').strip(),
                date_of_birth=dob,
                marital_status=request.form.get('marital_status', ''),
                occupation=request.form.get('occupation', '').strip(),
                monthly_income=Decimal(request.form.get('monthly_income', '0')),
                payment_type=request.form.get('payment_type', 'cash'),
                housing_status=request.form.get('housing_status', 'rent'),
                grant_amount=grant_amount,
                reason=request.form.get('reason', '').strip(),
                supporting_details=request.form.get('supporting_details', '').strip(),
                id_document_path=id_document_path,
                id_document_back_path=id_document_back_path,
            )
            db.session.add(app_obj)
            db.session.commit()
            
            # Create admin notification for new application
            notification = AdminNotification(
                notification_type='new_application',
                reference_id=app_obj.id,
                message=f'New application submitted by {current_user.name}'
            )
            db.session.add(notification)
            db.session.commit()
            
            # Send confirmation email
            try:
                email_sent = send_application_confirmation(
                    user_email=current_user.email,
                    user_name=current_user.name,
                    application_id=app_obj.get_reference_id(),
                    grant_amount=grant_amount
                )
                if email_sent:
                    print(f"[APPLICATION] Confirmation email sent successfully to {current_user.email}")
                else:
                    print(f"[APPLICATION] Warning: Confirmation email failed to send to {current_user.email}")
            except Exception as email_error:
                print(f"[APPLICATION] Email error: {str(email_error)}")
                # Don't fail the application if email fails
            
            flash('Application submitted successfully! Check your email for confirmation.', 'success')
            return redirect(url_for('user.dashboard'))

        except (ValueError, Exception) as e:
            flash(f'Error submitting application: {str(e)}', 'danger')
            return render_template('user/apply.html', form_data=request.form)

    return render_template('user/apply.html', form_data={})


@user_bp.route('/chat')
@login_required
def chat():
    if current_user.is_admin():
        return redirect(url_for('admin.chat'))

    admin = User.query.filter_by(role='admin').first()
    messages = []
    if admin:
        # Mark received messages as read
        Message.query.filter_by(
            sender_id=admin.id,
            recipient_id=current_user.id,
            is_read=False
        ).update({'is_read': True})
        db.session.commit()

        messages = Message.query.filter(
            db.or_(
                db.and_(Message.sender_id == current_user.id, Message.recipient_id == admin.id),
                db.and_(Message.sender_id == admin.id, Message.recipient_id == current_user.id),
            )
        ).order_by(Message.timestamp.asc()).all()

    return render_template('user/chat.html', messages=messages, admin=admin)
