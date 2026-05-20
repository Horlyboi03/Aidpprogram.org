#!/usr/bin/env python
"""
Test script to verify Gmail SMTP configuration
Run this to test if emails can be sent
"""

import os
from dotenv import load_dotenv
from flask_mail import Mail, Message
from flask import Flask

# Load environment variables
load_dotenv()

# Create a minimal Flask app for testing
app = Flask(__name__)

# Configure email settings from .env
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', True)
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@aidp.org')

# Initialize mail
mail = Mail(app)

def test_email():
    """Test sending an email"""
    print("=" * 70)
    print("GMAIL SMTP TEST")
    print("=" * 70)
    
    # Check configuration
    print("\n[1] Checking Configuration:")
    print(f"    MAIL_SERVER: {app.config['MAIL_SERVER']}")
    print(f"    MAIL_PORT: {app.config['MAIL_PORT']}")
    print(f"    MAIL_USE_TLS: {app.config['MAIL_USE_TLS']}")
    print(f"    MAIL_USERNAME: {app.config['MAIL_USERNAME']}")
    print(f"    MAIL_PASSWORD: {'*' * len(app.config['MAIL_PASSWORD']) if app.config['MAIL_PASSWORD'] else 'NOT SET'}")
    
    if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
        print("\n❌ ERROR: MAIL_USERNAME or MAIL_PASSWORD not set in .env file")
        return False
    
    # Try to send test email
    print("\n[2] Attempting to send test email...")
    
    try:
        with app.app_context():
            msg = Message(
                subject="AIDP Email Test",
                recipients=[app.config['MAIL_USERNAME']],
                sender=app.config.get('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME']),
                html="""
                <html>
                    <body style="font-family: Arial, sans-serif;">
                        <h2>✓ Email Configuration Test</h2>
                        <p>If you received this email, your Gmail SMTP configuration is working correctly!</p>
                        <p><strong>Next Steps:</strong></p>
                        <ol>
                            <li>Restart the AIDP application</li>
                            <li>Create a new user account</li>
                            <li>You should receive a welcome email</li>
                        </ol>
                        <p>Best regards,<br>AIDP System</p>
                    </body>
                </html>
                """
            )
            mail.send(msg)
            print("✓ Email sent successfully!")
            print(f"   Sent to: {app.config['MAIL_USERNAME']}")
            print("\n✓ Your Gmail SMTP configuration is working!")
            print("\nNext steps:")
            print("  1. Restart the AIDP application")
            print("  2. Create a new user account")
            print("  3. Check your email for the welcome message")
            return True
            
    except Exception as e:
        print(f"❌ ERROR: Failed to send email")
        print(f"   Error: {str(e)}")
        print("\nTroubleshooting:")
        print("  1. Check that MAIL_PASSWORD is correct (16-character app password)")
        print("  2. Make sure 2-Step Verification is enabled on your Gmail account")
        print("  3. Verify the password has no extra spaces")
        print("  4. Try the 'Less secure app access' method if app passwords don't work")
        print("  5. Check: https://myaccount.google.com/lesssecureapps")
        return False

if __name__ == '__main__':
    success = test_email()
    print("\n" + "=" * 70)
    if success:
        print("STATUS: ✓ CONFIGURATION OK")
    else:
        print("STATUS: ❌ CONFIGURATION FAILED")
    print("=" * 70)
