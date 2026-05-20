#!/usr/bin/env python3
"""
Send Admin Credentials Email
Sends the admin login link, username, and password separately to the admin email
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from flask_mail import Mail, Message

# Create Flask app
app = create_app()
mail = Mail(app)

def send_admin_credentials():
    """Send admin credentials to the configured admin email"""
    
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@aidp.org')
    admin_username = os.environ.get('ADMIN_EMAIL', 'admin@aidp.org')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'Admin@1234')
    app_url = os.environ.get('APP_URL', 'http://127.0.0.1:5000')
    login_url = f"{app_url}/auth/login"
    
    # Email 1: Login Link
    msg_link = Message(
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
                <p style="color: #666; line-height: 1.6;">
                    Click the button below to access the AIDP Admin Portal:
                </p>
                <div style="text-align: center; margin: 20px 0;">
                    <a href="{login_url}" style="display: inline-block; background: #4f8ef7; color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px;">
                        Access Admin Portal
                    </a>
                </div>
                <p style="color: #999; font-size: 12px; text-align: center;">
                    Or copy this link: <br/>
                    <code style="background: #e0e0e0; padding: 8px 12px; border-radius: 4px; display: inline-block; margin-top: 8px; word-break: break-all;">
                        {login_url}
                    </code>
                </p>
            </div>
            
            <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
                <p style="margin: 0; color: #856404; font-size: 14px;">
                    <strong>⚠️ Security Note:</strong> Your username and password will be sent in separate emails for security purposes.
                </p>
            </div>
            
            <div style="color: #999; font-size: 12px; text-align: center; padding-top: 20px; border-top: 1px solid #ddd;">
                <p style="margin: 10px 0;">This is an automated message from AIDP</p>
                <p style="margin: 0;">If you did not request this, please contact support immediately.</p>
            </div>
        </div>
        """
    )
    
    # Email 2: Username
    msg_username = Message(
        subject='👤 AIDP Admin - Username',
        recipients=[admin_email],
        html=f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #4f8ef7, #8b5cf6); padding: 30px; border-radius: 12px; text-align: center; color: white; margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 28px;">👤 Your Admin Username</h1>
            </div>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                <p style="color: #666; line-height: 1.6; margin-bottom: 20px;">
                    Your admin portal username is:
                </p>
                <div style="background: white; border: 2px solid #4f8ef7; padding: 15px; border-radius: 6px; text-align: center; margin-bottom: 20px;">
                    <p style="margin: 0; font-size: 18px; font-weight: bold; color: #4f8ef7; font-family: 'Courier New', monospace;">
                        {admin_username}
                    </p>
                </div>
                <p style="color: #666; font-size: 14px;">
                    Keep this username safe and secure. You will need it to log in to the admin portal.
                </p>
            </div>
            
            <div style="background: #e8f5e9; border-left: 4px solid #4caf50; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
                <p style="margin: 0; color: #2e7d32; font-size: 14px;">
                    <strong>✓ Security:</strong> Your password will be sent in a separate email.
                </p>
            </div>
            
            <div style="color: #999; font-size: 12px; text-align: center; padding-top: 20px; border-top: 1px solid #ddd;">
                <p style="margin: 10px 0;">This is an automated message from AIDP</p>
            </div>
        </div>
        """
    )
    
    # Email 3: Password
    msg_password = Message(
        subject='🔑 AIDP Admin - Password',
        recipients=[admin_email],
        html=f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #4f8ef7, #8b5cf6); padding: 30px; border-radius: 12px; text-align: center; color: white; margin-bottom: 20px;">
                <h1 style="margin: 0; font-size: 28px;">🔑 Your Admin Password</h1>
            </div>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                <p style="color: #666; line-height: 1.6; margin-bottom: 20px;">
                    Your admin portal password is:
                </p>
                <div style="background: white; border: 2px solid #4f8ef7; padding: 15px; border-radius: 6px; text-align: center; margin-bottom: 20px;">
                    <p style="margin: 0; font-size: 18px; font-weight: bold; color: #4f8ef7; font-family: 'Courier New', monospace; letter-spacing: 2px;">
                        {admin_password}
                    </p>
                </div>
                <p style="color: #666; font-size: 14px;">
                    Keep this password secure and confidential. Do not share it with anyone.
                </p>
            </div>
            
            <div style="background: #ffebee; border-left: 4px solid #f44336; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
                <p style="margin: 0; color: #c62828; font-size: 14px;">
                    <strong>⚠️ Important:</strong> Change your password immediately after your first login for security.
                </p>
            </div>
            
            <div style="background: #e3f2fd; border-left: 4px solid #2196f3; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
                <p style="margin: 0; color: #1565c0; font-size: 14px;">
                    <strong>ℹ️ Next Steps:</strong>
                </p>
                <ul style="margin: 10px 0 0 0; padding-left: 20px; color: #1565c0; font-size: 14px;">
                    <li>Use the login link from the first email</li>
                    <li>Enter your username and password</li>
                    <li>Change your password to something unique</li>
                    <li>Start managing applications</li>
                </ul>
            </div>
            
            <div style="color: #999; font-size: 12px; text-align: center; padding-top: 20px; border-top: 1px solid #ddd;">
                <p style="margin: 10px 0;">This is an automated message from AIDP</p>
                <p style="margin: 0;">If you did not request this, please contact support immediately.</p>
            </div>
        </div>
        """
    )
    
    try:
        mail.send(msg_link)
        print("✓ Login link email sent successfully")
        
        mail.send(msg_username)
        print("✓ Username email sent successfully")
        
        mail.send(msg_password)
        print("✓ Password email sent successfully")
        
        print("\n✅ All admin credentials emails sent to:", admin_email)
        print("\nAdmin Details:")
        print(f"  Email: {admin_email}")
        print(f"  Username: {admin_username}")
        print(f"  Password: {admin_password}")
        print(f"  Login URL: {login_url}")
        
    except Exception as e:
        print(f"❌ Error sending emails: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("AIDP Admin Credentials Email Sender")
    print("=" * 60)
    print()
    
    # Use app context
    with app.app_context():
        success = send_admin_credentials()
        
        if success:
            print("\n" + "=" * 60)
            print("✅ Admin credentials sent successfully!")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("❌ Failed to send admin credentials")
            print("=" * 60)
