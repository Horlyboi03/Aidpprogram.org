"""
Email utilities for AIDP application
"""
from flask_mail import Mail, Message
from flask import current_app, render_template_string
import os

mail = Mail()

# Email sending enabled/disabled flag
EMAIL_ENABLED = os.environ.get('EMAIL_ENABLED', 'false').lower() in ['true', '1', 'yes']


def send_application_confirmation(user_email, user_name, application_id, grant_amount):
    """Send application confirmation email to applicant"""
    print(f"[EMAIL] Attempting to send confirmation to {user_email}, EMAIL_ENABLED={EMAIL_ENABLED}")
    
    if not EMAIL_ENABLED:
        print(f"[EMAIL DISABLED] Would send application confirmation to {user_email}")
        return True
        
    subject = f"Application Confirmation - AIDP Grant Application {application_id}"
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #4f8ef7;">Application Received ✓</h2>
                
                <p>Dear {user_name},</p>
                
                <p>Thank you for submitting your grant application to the Agency for International Development Programs (AIDP).</p>
                
                <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <p><strong>Application Details:</strong></p>
                    <p>Application ID: <strong>{application_id}</strong></p>
                    <p>Grant Amount Requested: <strong>${grant_amount:,.0f}</strong></p>
                    <p>Status: <strong>Under Review</strong></p>
                </div>
                
                <p><strong>What happens next?</strong></p>
                <ul>
                    <li>Our team will review your application within 24-48 hours</li>
                    <li>You will receive an update via email and in your dashboard</li>
                    <li>You can track your application status anytime by logging into your account</li>
                    <li>Feel free to contact us via the chat feature if you have any questions</li>
                </ul>
                
                <p><strong>Important Reminder:</strong></p>
                <p>Once your application is approved, a processing fee will be required before your grant is disbursed. This is a real and legitimate fee charged by our processing partners.</p>
                
                <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd;">
                    Best regards,<br>
                    <strong>AIDP Team</strong><br>
                    Agency for International Development Programs
                </p>
                
                <p style="font-size: 12px; color: #999; margin-top: 20px;">
                    This is an automated email. Please do not reply to this message. 
                    Contact us through your dashboard chat for support.
                </p>
            </div>
        </body>
    </html>
    """
    
    msg = Message(
        subject=subject,
        recipients=[user_email],
        html=html_body
    )
    
    try:
        mail.send(msg)
        print(f"[EMAIL] Application confirmation sent to {user_email}")
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send application confirmation to {user_email}: {str(e)}")
        return False


def send_application_approved(user_email, user_name, application_id, grant_amount):
    """Send application approved email"""
    print(f"[EMAIL] Attempting to send approval to {user_email}, EMAIL_ENABLED={EMAIL_ENABLED}")
    
    if not EMAIL_ENABLED:
        print(f"[EMAIL DISABLED] Would send approval email to {user_email}")
        return True
        
    subject = f"Application Approved! - AIDP Grant {application_id}"
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #22c55e;">🎉 Congratulations! Your Application is Approved</h2>
                
                <p>Dear {user_name},</p>
                
                <p>We are pleased to inform you that your grant application has been <strong>APPROVED</strong>!</p>
                
                <div style="background: #e8f5e9; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #22c55e;">
                    <p><strong>Grant Details:</strong></p>
                    <p>Application ID: <strong>{application_id}</strong></p>
                    <p>Grant Amount Approved: <strong>${grant_amount:,.0f}</strong></p>
                </div>
                
                <p><strong>Next Steps:</strong></p>
                <ol>
                    <li>A processing fee will be calculated based on your grant amount</li>
                    <li>You will receive details about the processing fee via email and dashboard</li>
                    <li>Once the processing fee is paid and verified, your grant will be disbursed within 24-48 hours</li>
                    <li>Funds will be transferred to your preferred payment method (cash or cheque)</li>
                </ol>
                
                <p style="margin-top: 30px; padding: 15px; background: #fff3cd; border-radius: 8px;">
                    <strong>Important:</strong> Please log into your dashboard to view complete details and proceed with the next steps.
                </p>
                
                <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd;">
                    Best regards,<br>
                    <strong>AIDP Team</strong><br>
                    Agency for International Development Programs
                </p>
            </div>
        </body>
    </html>
    """
    
    msg = Message(
        subject=subject,
        recipients=[user_email],
        html=html_body
    )
    
    try:
        mail.send(msg)
        print(f"[EMAIL] Application approved email sent to {user_email}")
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send approval email to {user_email}: {str(e)}")
        return False


def send_application_rejected(user_email, user_name, application_id):
    """Send application rejected email"""
    print(f"[EMAIL] Attempting to send rejection to {user_email}, EMAIL_ENABLED={EMAIL_ENABLED}")
    
    if not EMAIL_ENABLED:
        print(f"[EMAIL DISABLED] Would send rejection email to {user_email}")
        return True
        
    subject = f"Application Status Update - AIDP Grant {application_id}"
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #ef4444;">Application Status Update</h2>
                
                <p>Dear {user_name},</p>
                
                <p>Thank you for your interest in the AIDP grant program. After careful review of your application, we regret to inform you that it does not meet the current eligibility criteria.</p>
                
                <div style="background: #fee; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ef4444;">
                    <p><strong>Application ID:</strong> {application_id}</p>
                    <p><strong>Status:</strong> Not Approved</p>
                </div>
                
                <p><strong>What you can do:</strong></p>
                <ul>
                    <li>Contact our support team via the chat feature for detailed feedback</li>
                    <li>You may reapply in the future if your circumstances change</li>
                    <li>Review the eligibility requirements on our website</li>
                </ul>
                
                <p>We appreciate your application and encourage you to reach out if you have any questions.</p>
                
                <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd;">
                    Best regards,<br>
                    <strong>AIDP Team</strong><br>
                    Agency for International Development Programs
                </p>
            </div>
        </body>
    </html>
    """
    
    msg = Message(
        subject=subject,
        recipients=[user_email],
        html=html_body
    )
    
    try:
        mail.send(msg)
        print(f"[EMAIL] Application rejected email sent to {user_email}")
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send rejection email to {user_email}: {str(e)}")
        return False


def send_welcome_email(user_email, user_name):
    """Send welcome email to new registered users"""
    if not EMAIL_ENABLED:
        print(f"[EMAIL DISABLED] Would send welcome email to {user_email}")
        return True
        
    subject = "Welcome to AIDP - Your Journey to Financial Empowerment Starts Here!"
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #4f8ef7;">Welcome to AIDP! 🌍</h2>
                
                <p>Dear {user_name},</p>
                
                <p>Thank you for creating an account with the Agency for International Development Programs (AIDP). We're excited to help you access grant funding between <strong>$100,000 – $450,000</strong> to transform your life and community.</p>
                
                <div style="background: #f0f4ff; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #4f8ef7;">
                    <h3 style="color: #4f8ef7; margin-top: 0;">What You Can Do Now:</h3>
                    <ul style="margin: 10px 0;">
                        <li><strong>Apply for a Grant:</strong> Complete your application in just 10-15 minutes</li>
                        <li><strong>Track Your Status:</strong> Monitor your application in real-time from your dashboard</li>
                        <li><strong>Chat with Support:</strong> Get instant help from our grant advisors</li>
                        <li><strong>Receive Updates:</strong> Get notified about your application status via email</li>
                    </ul>
                </div>
                
                <p><strong>Key Benefits of AIDP Grants:</strong></p>
                <ul>
                    <li>✓ <strong>Not a Loan:</strong> Grants don't need to be repaid</li>
                    <li>✓ <strong>Tax-Free:</strong> Grant money is not taxable</li>
                    <li>✓ <strong>No Credit Checks:</strong> Bad credit won't disqualify you</li>
                    <li>✓ <strong>Your Right:</strong> As a taxpayer, you have the right to apply</li>
                    <li>✓ <strong>Fast Review:</strong> Expert review as soon as possible</li>
                </ul>
                
                <p><strong>Getting Started:</strong></p>
                <ol>
                    <li>Log into your dashboard</li>
                    <li>Click "Apply for Grant"</li>
                    <li>Fill out the application form (takes 10-15 minutes)</li>
                    <li>Submit and wait for our team's review</li>
                    <li>Receive updates via email and dashboard</li>
                </ol>
                
                <p style="margin-top: 30px; padding: 15px; background: #e8f5e9; border-radius: 8px; border-left: 4px solid #22c55e;">
                    <strong>💡 Pro Tip:</strong> The sooner you apply, the sooner you can receive your grant. Our team reviews applications as soon as possible!
                </p>
                
                <p style="margin-top: 30px;">
                    If you have any questions or need assistance, our support team is available 24/7 through the chat feature in your dashboard.
                </p>
                
                <p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd;">
                    Best regards,<br>
                    <strong>AIDP Team</strong><br>
                    Agency for International Development Programs<br>
                    <em>Empowering communities. Changing lives.</em>
                </p>
                
                <p style="font-size: 12px; color: #999; margin-top: 20px;">
                    This is an automated email. Please do not reply to this message. 
                    Contact us through your dashboard chat for support.
                </p>
            </div>
        </body>
    </html>
    """
    
    msg = Message(
        subject=subject,
        recipients=[user_email],
        html=html_body
    )
    
    try:
        mail.send(msg)
        print(f"[EMAIL] Welcome email sent to {user_email}")
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send welcome email to {user_email}: {str(e)}")
        return False
