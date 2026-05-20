# 📧 Email Notification System - Activation Guide

## ✅ Current Status

**Flask-Mail is FULLY INTEGRATED and ready to use!**

The application already has complete email functionality built-in:

### Email Notifications Already Implemented:

1. ✅ **Welcome Email** - Sent when new users register
2. ✅ **Application Confirmation** - Sent immediately when applicant submits application
3. ✅ **Application Approved** - Sent when admin approves an application
4. ✅ **Application Rejected** - Sent when admin rejects an application

### Current State:
- Email system is **DISABLED** (`EMAIL_ENABLED=false` in `.env`)
- All email attempts are logged to console instead of being sent
- You'll see messages like: `[EMAIL DISABLED] Would send application confirmation to user@email.com`

---

## 🚀 How to Enable Email Notifications

You need to configure a valid email service. Here are your options:

### Option 1: Gmail (Recommended for Testing)

**Requirements:**
- A Gmail account
- 2-Factor Authentication enabled on your Google account
- An App Password generated

**Steps:**

1. **Enable 2-Factor Authentication:**
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Click "Generate"
   - Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

3. **Update `.env` file:**
   ```env
   EMAIL_ENABLED=true
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=maryygeorge193@gmail.com
   MAIL_PASSWORD=your-16-char-app-password-here
   MAIL_DEFAULT_SENDER=maryygeorge193@gmail.com
   ```

4. **Restart the Flask server**

---

### Option 2: SendGrid (Recommended for Production)

**Requirements:**
- SendGrid account (free tier: 100 emails/day)
- API Key

**Steps:**

1. **Sign up at SendGrid:**
   - Go to https://signup.sendgrid.com/
   - Create a free account

2. **Create API Key:**
   - Go to Settings → API Keys
   - Click "Create API Key"
   - Give it "Full Access" or "Mail Send" permission
   - Copy the API key (starts with `SG.`)

3. **Update `.env` file:**
   ```env
   EMAIL_ENABLED=true
   MAIL_SERVER=smtp.sendgrid.net
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=apikey
   MAIL_PASSWORD=SG.your-sendgrid-api-key-here
   MAIL_DEFAULT_SENDER=maryygeorge193@gmail.com
   ```

4. **Verify sender email in SendGrid:**
   - Go to Settings → Sender Authentication
   - Verify your email address (maryygeorge193@gmail.com)

5. **Restart the Flask server**

---

### Option 3: Other SMTP Services

You can use any SMTP service:

- **Outlook/Hotmail:** `smtp-mail.outlook.com:587`
- **Yahoo:** `smtp.mail.yahoo.com:587`
- **Custom SMTP:** Use your hosting provider's SMTP settings

Update `.env` with the appropriate settings:
```env
EMAIL_ENABLED=true
MAIL_SERVER=your-smtp-server.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@domain.com
MAIL_PASSWORD=your-password
MAIL_DEFAULT_SENDER=your-email@domain.com
```

---

## 🧪 Testing Email Functionality

After enabling emails, test the system:

### Test 1: Welcome Email
1. Register a new user account
2. Check the email inbox for welcome message
3. Console should show: `[EMAIL] Welcome email sent to user@email.com`

### Test 2: Application Confirmation
1. Log in as a regular user
2. Submit a grant application
3. Check email for confirmation message
4. Console should show: `[EMAIL] Application confirmation sent to user@email.com`

### Test 3: Approval/Rejection Emails
1. Log in as admin (maryygeorge193@gmail.com / Horlyboi1607)
2. Approve or reject an application
3. Check applicant's email for notification
4. Console should show: `[EMAIL] Application approved/rejected email sent to user@email.com`

---

## 📝 Email Templates

All email templates are in `app/email.py` and include:

- **Professional HTML formatting**
- **AIDP branding and colors**
- **Clear call-to-action buttons**
- **Application details and next steps**
- **Contact information**

You can customize the email content by editing the functions in `app/email.py`:
- `send_welcome_email()`
- `send_application_confirmation()`
- `send_application_approved()`
- `send_application_rejected()`

---

## 🔧 Troubleshooting

### Emails not sending?

1. **Check console output:**
   - Look for `[EMAIL ERROR]` messages
   - Error messages will show what went wrong

2. **Common issues:**
   - **"Authentication failed"** → Wrong password or username
   - **"Connection refused"** → Wrong MAIL_SERVER or MAIL_PORT
   - **"Sender not verified"** → Need to verify sender email in SendGrid
   - **"App password required"** → Gmail needs app password, not regular password

3. **Verify settings:**
   ```bash
   # Check if EMAIL_ENABLED is true
   cat .env | grep EMAIL_ENABLED
   
   # Check MAIL_USERNAME
   cat .env | grep MAIL_USERNAME
   ```

4. **Test SMTP connection:**
   ```python
   # Run this in Python console
   from flask_mail import Mail, Message
   from app import create_app
   
   app = create_app()
   with app.app_context():
       mail = Mail(app)
       msg = Message("Test", recipients=["test@example.com"])
       mail.send(msg)
   ```

---

## 🎯 Quick Start (Gmail)

**Fastest way to enable emails:**

1. Generate Gmail App Password: https://myaccount.google.com/apppasswords
2. Edit `.env`:
   ```env
   EMAIL_ENABLED=true
   MAIL_PASSWORD=your-16-char-app-password
   ```
3. Restart server: `python run.py`
4. Test by registering a new user

---

## 📊 Email Logs

When emails are sent, you'll see console logs:

```
[EMAIL] Welcome email sent to john@example.com
[EMAIL] Application confirmation sent to jane@example.com
[EMAIL] Application approved email sent to bob@example.com
```

When emails fail:
```
[EMAIL ERROR] Failed to send welcome email to user@example.com: Authentication failed
```

When emails are disabled:
```
[EMAIL DISABLED] Would send application confirmation to user@example.com
```

---

## ✨ Summary

**Everything is ready!** Just:
1. Choose an email service (Gmail recommended for testing)
2. Get credentials (App Password for Gmail)
3. Update `.env` with `EMAIL_ENABLED=true` and credentials
4. Restart the server
5. Test by registering a new user or submitting an application

**No code changes needed** - the email system is fully integrated and waiting to be activated!
