"""
Admin routes: dashboard, users, applications, chat
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app import db, csrf
from app.models import Application, User, Message, AdminNotification
from app.email import send_application_approved, send_application_rejected

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    """Decorator to restrict routes to admin users only."""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated


def get_admin_notifications():
    """Get notification counts for admin."""
    if not current_user.is_authenticated or not current_user.is_admin():
        return {'unread_messages': 0, 'pending_applications': 0, 'unread_notifications': 0}
    
    # Count unread messages from all applicants
    unread_messages = Message.query.filter_by(
        recipient_id=current_user.id,
        is_read=False
    ).count()
    
    # Count pending applications
    pending_applications = Application.query.filter_by(status='pending').count()
    
    # Count unread admin notifications
    unread_notifications = AdminNotification.query.filter_by(is_read=False).count()
    
    return {
        'unread_messages': unread_messages,
        'pending_applications': pending_applications,
        'unread_notifications': unread_notifications
    }


@admin_bp.context_processor
def inject_notifications():
    """Inject notification counts into all admin templates."""
    if current_user.is_authenticated and current_user.is_admin():
        return {'admin_notifications': get_admin_notifications()}
    return {'admin_notifications': {'unread_messages': 0, 'pending_applications': 0, 'unread_notifications': 0}}


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_users = User.query.filter_by(role='applicant').count()
    total_apps = Application.query.count()
    pending = Application.query.filter_by(status='pending').count()
    approved = Application.query.filter_by(status='approved').count()
    rejected = Application.query.filter_by(status='rejected').count()
    
    # Support filtering by status via query parameter
    status_filter = request.args.get('status', 'all')
    query = Application.query
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    recent_apps = query.order_by(Application.created_at.desc()).limit(10).all()

    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        total_apps=total_apps,
        pending=pending,
        approved=approved,
        rejected=rejected,
        recent_apps=recent_apps,
        status_filter=status_filter,
    )


@admin_bp.route('/test-cache')
def test_cache():
    """Test page to verify cache is cleared"""
    return render_template('test_cache.html')


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    users_list = User.query.filter_by(role='applicant').order_by(
        User.created_at.desc()
    ).paginate(page=page, per_page=15)
    return render_template('admin/users.html', users=users_list)


@admin_bp.route('/applications')
@login_required
@admin_required
def applications():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')
    search_query = request.args.get('search', '').strip()

    query = Application.query
    
    # Filter by status
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    # Search by application reference ID, full name, or email
    if search_query:
        query = query.filter(
            db.or_(
                Application.reference_id.ilike(f'%{search_query}%'),
                Application.full_name.ilike(f'%{search_query}%'),
                Application.email.ilike(f'%{search_query}%')
            )
        )

    apps = query.order_by(Application.created_at.desc()).paginate(page=page, per_page=10)
    
    # Mark all new application notifications as read when viewing applications page
    AdminNotification.query.filter_by(
        notification_type='new_application',
        is_read=False
    ).update({'is_read': True})
    db.session.commit()
    
    return render_template('admin/applications.html', apps=apps, status_filter=status_filter, search_query=search_query)


@admin_bp.route('/application/<int:app_id>')
@login_required
@admin_required
def view_application(app_id):
    application = Application.query.get_or_404(app_id)
    
    # Mark notification as read when viewing the application
    notification = AdminNotification.query.filter_by(
        notification_type='new_application',
        reference_id=app_id,
        is_read=False
    ).first()
    if notification:
        notification.is_read = True
        db.session.commit()
    
    return render_template('admin/view_application.html', application=application)


@admin_bp.route('/application/<int:app_id>/panel')
@login_required
@admin_required
def view_application_panel(app_id):
    """Return application details as a slide-in panel (AJAX)"""
    application = Application.query.get_or_404(app_id)
    return render_template('admin/application_panel.html', application=application)


@admin_bp.route('/application/<int:app_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_application(app_id):
    application = Application.query.get_or_404(app_id)
    application.status = 'approved'
    application.reviewed_at = datetime.utcnow()
    db.session.commit()
    
    # Send approval email
    user = User.query.get(application.user_id)
    if user:
        send_application_approved(
            user_email=user.email,
            user_name=user.name,
            application_id=application.id,
            grant_amount=application.grant_amount
        )
    
    flash(f'Application #{app_id} has been approved and email sent to applicant.', 'success')
    return redirect(url_for('admin.applications'))


@admin_bp.route('/application/<int:app_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_application(app_id):
    application = Application.query.get_or_404(app_id)
    application.status = 'rejected'
    application.reviewed_at = datetime.utcnow()
    db.session.commit()
    
    # Send rejection email
    user = User.query.get(application.user_id)
    if user:
        send_application_rejected(
            user_email=user.email,
            user_name=user.name,
            application_id=application.id
        )
    
    flash(f'Application #{app_id} has been rejected and email sent to applicant.', 'warning')
    return redirect(url_for('admin.applications'))


@admin_bp.route('/application/<int:app_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_application(app_id):
    application = Application.query.get_or_404(app_id)
    db.session.delete(application)
    db.session.commit()
    flash(f'Application #{app_id} has been deleted.', 'info')
    return redirect(url_for('admin.applications'))


@admin_bp.route('/chat')
@admin_bp.route('/chat/<int:user_id>')
@login_required
@admin_required
def chat(user_id=None):
    # Get all applicants who have messages with admin
    # Sort by most recent message (newest first)
    from sqlalchemy import func
    
    # Subquery to get the latest message timestamp for each user
    latest_message_subquery = db.session.query(
        db.case(
            (Message.sender_id == current_user.id, Message.recipient_id),
            else_=Message.sender_id
        ).label('user_id'),
        func.max(Message.timestamp).label('latest_timestamp')
    ).filter(
        db.or_(
            Message.sender_id == current_user.id,
            Message.recipient_id == current_user.id
        )
    ).group_by('user_id').subquery()
    
    # Get applicants with messages, ordered by latest message timestamp
    applicants_with_messages = db.session.query(User).join(
        latest_message_subquery,
        User.id == latest_message_subquery.c.user_id
    ).filter(
        User.role == 'applicant'
    ).order_by(latest_message_subquery.c.latest_timestamp.desc()).all()

    selected_user = None
    messages = []

    if user_id:
        selected_user = User.query.get_or_404(user_id)
        # Mark messages as read
        Message.query.filter_by(
            sender_id=user_id,
            recipient_id=current_user.id,
            is_read=False
        ).update({'is_read': True})
        db.session.commit()

        messages = Message.query.filter(
            db.or_(
                db.and_(Message.sender_id == current_user.id, Message.recipient_id == user_id),
                db.and_(Message.sender_id == user_id, Message.recipient_id == current_user.id),
            )
        ).order_by(Message.timestamp.asc()).all()

    # Unread count per user for sidebar badges
    unread_counts = {}
    for u in applicants_with_messages:
        unread_counts[u.id] = Message.query.filter_by(
            sender_id=u.id,
            recipient_id=current_user.id,
            is_read=False
        ).count()

    return render_template(
        'admin/chat.html',
        applicants=applicants_with_messages,
        selected_user=selected_user,
        messages=messages,
        unread_counts=unread_counts,
    )


@admin_bp.route('/chat/delete/<int:user_id>', methods=['POST'])
@csrf.exempt
@login_required
@admin_required
def delete_conversation(user_id):
    """Delete all messages in a conversation with a specific user."""
    from flask import jsonify
    import logging
    
    logger = logging.getLogger(__name__)
    logger.info(f'[DELETE] Request received for user_id: {user_id}')
    logger.info(f'[DELETE] Current user: {current_user.id} ({current_user.email})')
    
    try:
        # Verify the user exists
        user = User.query.get(user_id)
        if not user:
            logger.error(f'[DELETE] User {user_id} not found')
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        logger.info(f'[DELETE] Deleting conversation with {user.name} ({user.email})')
        
        # Delete all messages between admin and this user
        deleted_count = Message.query.filter(
            db.or_(
                db.and_(Message.sender_id == current_user.id, Message.recipient_id == user_id),
                db.and_(Message.sender_id == user_id, Message.recipient_id == current_user.id),
            )
        ).delete(synchronize_session=False)
        
        logger.info(f'[DELETE] Deleted {deleted_count} messages')
        
        db.session.commit()
        logger.info(f'[DELETE] Transaction committed successfully')
        
        return jsonify({
            'success': True, 
            'message': f'Conversation with {user.name} deleted successfully',
            'deleted_count': deleted_count
        })
    except Exception as e:
        logger.error(f'[DELETE] Error occurred: {str(e)}', exc_info=True)
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_bp.route('/api/notifications/count')
@login_required
@admin_required
def get_notification_count():
    """API endpoint to get current notification count."""
    notifications = get_admin_notifications()
    return jsonify(notifications)


@admin_bp.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403
