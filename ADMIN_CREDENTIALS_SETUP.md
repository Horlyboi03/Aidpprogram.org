# 🔐 AIDP Admin Credentials Setup

## How to Send Admin Login Credentials

### Method 1: Using the Python Script (Recommended)

1. **Make sure your `.env` file is configured** with email settings:
   ```
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ADMIN_EMAIL=admin@aidp.org
   ADMIN_PASSWORD=Admin@1234
   ```

2. **Run the script**:
   ```bash
   python send_admin_credentials.py
   ```

3. **What happens**:
   - Email 1: Login link to the admin portal
   - Email 2: Admin username
   - Email 3: Admin password
   - All sent separately for security

### Method 2: Manual Email

If you prefer to send manually, here are the credentials:

**Admin Portal URL:**
```
http://127.0.0.1:5000/auth/login
```

**Admin Email:**
```
admin@aidp.org
```

**Admin Username:**
```
admin@aidp.org
```

**Admin Password:**
```
Admin@1234
```

---

## 📋 Admin Portal Features

Once logged in, admins can:
- ✅ View all grant applications
- ✅ Review applicant details
- ✅ Approve or reject applications
- ✅ Chat with applicants
- ✅ View user management
- ✅ Access dashboard with statistics

---

## 🔒 Security Recommendations

1. **Change Password**: Admin should change password immediately after first login
2. **Keep Credentials Secure**: Never share username/password
3. **Use Strong Passwords**: Update to a unique, strong password
4. **Enable 2FA**: Consider adding two-factor authentication (future enhancement)

---

## 📧 Email Configuration

### Gmail Setup (Recommended)

1. Enable 2-Step Verification on your Google Account
2. Generate an App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the generated password
3. Use this password in `.env` as `MAIL_PASSWORD`

### Other Email Providers

- **Outlook**: Use your email and password
- **SendGrid**: Use `apikey` as username and your API key as password
- **Mailgun**: Configure SMTP settings from your Mailgun dashboard

---

## 🆘 Troubleshooting

**Emails not sending?**
- Check `.env` file has correct email configuration
- Verify MAIL_USERNAME and MAIL_PASSWORD are correct
- Check if Gmail requires app-specific password
- Ensure MAIL_SERVER and MAIL_PORT are correct

**Script not running?**
- Make sure you're in the project root directory
- Ensure Python 3.8+ is installed
- Install dependencies: `pip install -r requirements.txt`

---

## 📞 Support

For issues with admin setup, check:
1. Email configuration in `.env`
2. Database connection
3. Flask app is running properly
4. Check application logs for errors
