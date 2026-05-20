# 🚀 Quick Start: Send Admin Credentials Email

## Prerequisites

Make sure your `.env` file is configured with email settings:

```env
# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@aidp.org

# Admin Credentials
ADMIN_EMAIL=admin@aidp.org
ADMIN_PASSWORD=Admin@1234
ADMIN_NAME=AIDP Administrator

# App URL (optional, defaults to http://127.0.0.1:5000)
APP_URL=http://127.0.0.1:5000
```

## How to Send Admin Credentials

### Option 1: Simple Script (Recommended) ⭐

```bash
python send_admin_email_simple.py
```

This will:
- ✅ Send login link email
- ✅ Send username email
- ✅ Send password email
- ✅ Display confirmation with all details

### Option 2: Original Script

```bash
python send_admin_credentials.py
```

## What Admin Receives

The admin will receive **3 separate emails**:

### Email 1: 🔐 Login Link
- Contains the admin portal URL
- Direct link to login page
- Security notice about separate credentials

### Email 2: 👤 Username
- Admin username (email address)
- Security reminder
- Note that password comes separately

### Email 3: 🔑 Password
- Admin password
- Security warning to change password
- Instructions for first login

## Email Configuration Examples

### Gmail (Recommended)

1. Enable 2-Step Verification: https://myaccount.google.com/security
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Select "Mail" and "Windows Computer"
4. Copy the generated password
5. Use in `.env`:
   ```env
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=xxxx xxxx xxxx xxxx
   ```

### Outlook/Hotmail

```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
```

### SendGrid

```env
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=SG.your-api-key
```

## Troubleshooting

### Error: "No module named 'app'"
- Make sure you're running from the project root directory
- Check that `app/__init__.py` exists

### Error: "SMTP connection refused"
- Check MAIL_SERVER and MAIL_PORT are correct
- Verify internet connection
- Check firewall settings

### Error: "Authentication failed"
- Verify MAIL_USERNAME and MAIL_PASSWORD
- For Gmail, use app-specific password (not regular password)
- Check if 2-Step Verification is enabled

### Emails not received
- Check spam/junk folder
- Verify ADMIN_EMAIL is correct
- Check email configuration in `.env`
- Try sending a test email first

## Admin Portal Access

Once emails are sent, admin can:

1. **Click the login link** from first email
2. **Enter username** from second email
3. **Enter password** from third email
4. **Change password** on first login (recommended)

## Admin Portal Features

After login, admin can:
- 📊 View dashboard with statistics
- 📋 Review all applications
- ✅ Approve/Reject applications
- 💬 Chat with applicants
- 👥 Manage users
- 📈 View analytics

## Security Tips

1. **Change Password**: Admin should change password immediately
2. **Keep Credentials Safe**: Never share username/password
3. **Use Strong Password**: Update to unique, strong password
4. **Logout**: Always logout when done
5. **Monitor Activity**: Check admin logs regularly

## Need Help?

- Check `.env` file configuration
- Verify email settings are correct
- Check application logs for errors
- Ensure Flask app is running properly
- Review ADMIN_CREDENTIALS_SETUP.md for detailed guide

---

**That's it!** Your admin will receive all credentials in separate, secure emails. 🎉
