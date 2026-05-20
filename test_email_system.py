"""
Test Email System - Verify Flask-Mail Configuration
Run this script to test if your email settings are working correctly.
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_email_config():
    """Test email configuration and send a test email"""
    
    print("=" * 60)
    print("AIDP Email System Test")
    print("=" * 60)
    
    # Check if email is enabled
    email_enabled = os.environ.get('EMAIL_ENABLED', 'False').lower() == 'true'
    
    print(f"\n📧 Email Status: {'ENABLED ✅' if email_enabled else 'DISABLED ❌'}")
    
    if not email_enabled:
        print("\n⚠️  Email is currently DISABLED")
        print("To enable emails, set EMAIL_ENABLED=true in your .env file")
        print("\nCurrent .env settings:")
        print(f"  EMAIL_ENABLED={os.environ.get('EMAIL_ENABLED', 'not set')}")
        return
    
    # Display current configuration
    print("\n📋 Current Email Configuration:")
    print(f"  MAIL_SERVER: {os.environ.get('MAIL_SERVER', 'not set')}")
    print(f"  MAIL_PORT: {os.environ.get('MAIL_PORT', 'not set')}")
    print(f"  MAIL_USE_TLS: {os.environ.get('MAIL_USE_TLS', 'not set')}")
    print(f"  MAIL_USERNAME: {os.environ.get('MAIL_USERNAME', 'not set')}")
    print(f"  MAIL_PASSWORD: {'*' * 16 if os.environ.get('MAIL_PASSWORD') else 'not set'}")
    print(f"  MAIL_DEFAULT_SENDER: {os.environ.get('MAIL_DEFAULT_SENDER', 'not set')}")
    
    # Test email sending
    print("\n🧪 Testing email functionality...")
    
    try:
        from app import create_app
        from app.email import mail, send_welcome_email
        
        app = create_app()
        
        with app.app_context():
            # Test connection
            print("\n1️⃣ Testing SMTP connection...")
            
            # Get test recipient
            test_email = input("\nEnter email address to send test email to: ").strip()
            
            if not test_email:
                print("❌ No email address provided. Test cancelled.")
                return
            
            print(f"\n2️⃣ Sending test email to {test_email}...")
            
            from flask_mail import Message
            
            msg = Message(
                subject="AIDP Email System Test ✅",
                recipients=[test_email],
                html="""
                <html>
                    <body style="font-family: Arial, sans-serif; padding: 20px;">
                        <h2 style="color: #4f8ef7;">Email System Test Successful! ✅</h2>
                        <p>Your AIDP email configuration is working correctly.</p>
                        <p><strong>Configuration Details:</strong></p>
                        <ul>
                            <li>MAIL_SERVER: {}</li>
                            <li>MAIL_PORT: {}</li>
                            <li>MAIL_USERNAME: {}</li>
                        </ul>
                        <p>You can now send email notifications to applicants!</p>
                        <hr>
                        <p style="color: #999; font-size: 12px;">
                            This is a test email from AIDP Grant Management System
                        </p>
                    </body>
                </html>
                """.format(
                    os.environ.get('MAIL_SERVER'),
                    os.environ.get('MAIL_PORT'),
                    os.environ.get('MAIL_USERNAME')
                )
            )
            
            mail.send(msg)
            
            print("\n✅ SUCCESS! Test email sent successfully!")
            print(f"📬 Check the inbox for {test_email}")
            print("\n🎉 Your email system is configured correctly!")
            print("\nYou can now:")
            print("  • Send welcome emails to new users")
            print("  • Send application confirmations")
            print("  • Send approval/rejection notifications")
            
    except Exception as e:
        print(f"\n❌ ERROR: Failed to send test email")
        print(f"\nError details: {str(e)}")
        print("\n🔧 Troubleshooting tips:")
        print("  1. Check your MAIL_USERNAME and MAIL_PASSWORD in .env")
        print("  2. For Gmail, use an App Password (not your regular password)")
        print("  3. Verify MAIL_SERVER and MAIL_PORT are correct")
        print("  4. Check if your email provider requires additional setup")
        print("\n📖 See EMAIL_ACTIVATION_GUIDE.md for detailed setup instructions")


if __name__ == '__main__':
    test_email_config()
