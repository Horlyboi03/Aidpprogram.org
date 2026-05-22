"""
Authentication routes: register, login, logout
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User
from app.email import send_welcome_email

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        # --- Validation ---
        if not all([name, email, password, confirm]):
            flash('All fields are required.', 'danger')
            return render_template('auth/register.html')

        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'danger')
            return render_template('auth/register.html')

        if User.query.filter_by(email=email).first():
            flash('An account with that email already exists.', 'danger')
            return render_template('auth/register.html')

        # --- Create user ---
        user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            role='applicant',
        )
        db.session.add(user)
        db.session.commit()

        # Try to send welcome email (but don't fail registration if it doesn't work)
        try:
            send_welcome_email(user.email, user.name)
        except Exception as e:
            print(f"[REGISTER] Email error: {str(e)}")
        
        # Flash success message
        flash('Account created successfully! Please sign in with your credentials.', 'success')
        
        # Render a redirect page instead of using Flask redirect
        # This ensures the page loads properly on mobile
        return render_template('auth/register_success.html', login_url=url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid email or password.', 'danger')
            return render_template('auth/login.html')

        # Mark online
        user.is_online = True
        db.session.commit()

        login_user(user, remember=remember)

        next_page = request.args.get('next')
        if user.is_admin():
            return redirect(next_page or url_for('admin.dashboard'))
        return redirect(next_page or url_for('user.dashboard'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    current_user.is_online = False
    db.session.commit()
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
