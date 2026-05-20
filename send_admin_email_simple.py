#!/usr/bin/env python3
"""
Simple Admin Credentials Email Sender
Run this from the project root directory
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main function to send admin credentials"""
    
    # Import after path is set
    from app import create_app
    from flask_mail import Mail, Message
    
    # Create app and mail
    app = create_app()
    mail = Mail(app)
    
    # Get credentials from environment
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@aidp.org')
    admin_username = os.environ.get('ADMIN_EMAIL', 'admin@aidp.org')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'Admin@1234')
    app_url = os.environ.get('APP_URL', 'http://127.0.0.1:5000')
    login_url = f"{app_url}/auth/login"
    
    print("=" * 70)
    print("AIDP Admin Credentials Email Sender")
    print("=" * 70)
    print()
    print(f"📧 Sending credentials to: {admin_email}")
    print()
    
    # Use app context
    with app.app_context():
        try:
            # Email 1: Login Link
            msg1 = Message(
                subject='🔐 AIDP Admin Portal - Login Link',
                recipients=[admin_email],
                html=f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #4f8ef7, #8b5cf6); padding: 30px; border-radius: 12px; text-align: center; color: white; margin-bottom: 20px;">
                        <h1 style="margin: 0; font-size: 28px;">🔐 AIDP Admin Portal</h1>
                        <p style="margin: 10px 0 0 0; font-size: 14px; opacity: 0.9;">Secure Access Link</p>
                    </div>
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                        <h2 style="color: #333; margin-top: 0;">Admin Portal Access</h2>
                        <p style="color: #666; line-height: 1.6;">Click the button below to access the AIDP Admin Portal:</p>
                        <div style="text-align: center; margin: 20px 0;">
                            <a href="{login_url}" style="display: inline-block; background: #4f8ef7; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px;">Access Admin Portal</a>
                        </div>
                        <p style="color: #999; font-size: 12px; text-align: center;">Or copy: <code style="background: #e0e0e0; padding: 4px 8px; border-radius: 3px;">{login_url}</code></p>
                    </div>
                    <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; border-radius: 4px;">
                        <p style="margin: 0; color: #856404; font-size: 14px;"><strong>⚠️ Security:</strong> Your username and password will be sent in separate emails.</p>
                    </div>
                </div>
                """
            )
            mail.send(msg1)
            print("✓ Email 1 sent: Login link")
            
            # Email 2: Username
            msg2 = Message(
                subject='👤 AIDP Admin - Username',
                recipients=[admin_email],
                html=f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #4f8ef7, #8b5cf6); padding: 30px; border-radius: 12px; text-align: center; color: white; margin-bottom: 20px;">
                        <h1 style="margin: 0; font-size: 28px;">👤 Your Admin Username</h1>
                    </div>
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                        <p style="color: #666; line-height: 1.6; margin-bottom: 20px;">Your admin portal username is:</p>
                        <div style="background: white; border: 2px solid #4f8ef7; padding: 15px; border-radius: 6px; text-align: center; margin-bottom: 20px;">
                            <p style="margin: 0; font-size: 18px; font-weight: bold; color: #4f8ef7; font-family: 'Courier New', monospace;">{admin_username}</p>
                        </div>
                        <p style="color: #666; font-size: 14px;">Keep this username safe and secure.</p>
                    </div>
                    <div style="background: #e8f5e9; border-left: 4px solid #4caf50; padding: 15px; border-radius: 4px;">
                        <p style="margin: 0; color: #2e7d32; font-size: 14px;"><strong>✓ Security:</strong> Your password will be sent in a separate email.</p>
                    </div>
                </div>
                """
            )
            mail.send(msg2)
            print("✓ Email 2 sent: Username")
            
            # Email 3: Password
            msg3 = Message(
                subject='🔑 AIDP Admin - Password',
                recipients=[admin_email],
                html=f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #4f8ef7, #8b5cf6); padding: 30px; border-radius: 12px; text-align: center; color: white; margin-bottom: 20px;">
                        <h1 style="margin: 0; font-size: 28px;">🔑 Your Admin Password</h1>
                    </div>
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                        <p style="color: #666; line-height: 1.6; margin-bottom: 20px;">Your admin portal password is:</p>
                        <div style="background: white; border: 2px solid #4f8ef7; padding: 15px; border-radius: 6px; text-align: center; margin-bottom: 20px;">
                            <p style="margin: 0; font-size: 18px; font-weight: bold; color: #4f8ef7; font-family: 'Courier New', monospace; letter-spacing: 2px;">{admin_password}</p>
                        </div>
                        <p style="color: #666; font-size: 14px;">Keep this password secure and confidential.</p>
                    </div>
                    <div style="background: #ffebee; border-left: 4px solid #f44336; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
                        <p style="margin: 0; color: #c62828; font-size: 14px;"><strong>⚠️ Important:</strong> Change your password immediately after first login.</p>
                    </div>
                </div>
                """
            )
            mail.send(msg3)
            print("✓ Email 3 sent: Password")
            
            print()
            print("=" * 70)
            print("✅ All emails sent successfully!")
            print("=" * 70)
            print()
            print("Admin Details:")
            print(f"  Email:    {admin_email}")
            print(f"  Username: {admin_username}")
            print(f"  Password: {admin_password}")
            print(f"  Login:    {login_url}")
            print()
            
            return True
            
        except Exception as e:
            print()
            print("=" * 70)
            print(f"❌ Error: {str(e)}")
            print("=" * 70)
            print()
            print("Troubleshooting:")
            print("1. Check .env file has correct email configuration")
            print("2. Verify MAIL_USERNAME and MAIL_PASSWORD are correct")
            print("3. For Gmail, use an app-specific password")
            print("4. Check internet connection")
            print()
            return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
