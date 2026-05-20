# Email Configuration Guide for AIDP

## Issue
Emails are not being sent from the application. The error indicates: "Username and Password not accepted" from Gmail SMTP.

## Solution

Gmail requires an **App Password** instead of your regular account password when using SMTP. Follow these detailed steps:

---

## STEP-BY-STEP GUIDE TO ENABLE 2-FACTOR AUTHENTICATION & GET APP PASSWORD

### Step 1: Go to Google Account Security Settings
1. Open your browser and go to: **https://myaccount.google.com/security**
2. You may need to log in with your Gmail account (maryygeorge193@gmail.com)
3. Look for the left sidebar menu

### Step 2: Enable 2-Step Verification
1. In the left sidebar, find **"2-Step Verification"** (or "2-Factor Authentication")
2. Click on it
3. Click the **"Get Started"** button
4. Follow Google's prompts:
   - Enter your password
   - Choose a recovery phone number
   - Google will send a verification code to your phone
   - Enter the code to confirm
5. Complete the setup

**Note:** If you don't see "2-Step Verification" option, scroll down in the security settings page.

### Step 3: Generate App Password
1. After 2-Step Verification is enabled, go back to: **https://myaccount.google.com/security**
2. In the left sidebar, scroll down and look for **"App passwords"** (this ONLY appears after 2FA is enabled)
3. If you still don't see it:
   - Make sure 2-Step Verification is fully enabled
   - Try refreshing the page
   - Try a different browser
4. Click on **"App passwords"**
5. You'll see a dropdown menu asking:
   - **Select the app:** Choose "Mail"
   - **Select the device:** Choose "Windows Computer" (or your device type)
6. Click **"Generate"**
7. Google will show you a 16-character password like: `xxxx xxxx xxxx xxxx`
8. **Copy this password** (including the spaces)

### Step 4: Update .env File
1. Open the `.env` file in your project
2. Find the line: `MAIL_PASSWORD=kkbrbqcovywnzmgl`
3. Replace it with the 16-character password you just copied:
   ```
   MAIL_PASSWORD=xxxx xxxx xxxx xxxx
   ```
4. **Keep the spaces** in the password
5. Save the file

### Step 5: Restart the Application
1. Stop your Flask application (if running)
2. Restart it
3. The new password will be loaded from the .env file

### Step 6: Test Email Sending
1. Create a new user account on the application
2. Check your email inbox for the welcome email
3. If you receive it, emails are working!
4. If not, check spam/junk folder

---

## TROUBLESHOOTING

### "I don't see App passwords option"
**Solution:** 2-Step Verification is not enabled
- Go to https://myaccount.google.com/security
- Enable "2-Step Verification" first
- Wait a few minutes
- Then look for "App passwords"

### "I enabled 2FA but still don't see App passwords"
**Solution:** Try these steps:
1. Refresh the page (Ctrl+R or Cmd+R)
2. Try a different browser (Chrome, Firefox, Edge)
3. Clear your browser cache
4. Log out and log back in to Google Account

### "Still not receiving emails after updating password"
**Solution:** Check these:
1. Verify the password is exactly 16 characters (with spaces)
2. Check your spam/junk folder
3. Restart the Flask application
4. Check application logs for `[EMAIL ERROR]` messages
5. Make sure you saved the .env file

### "I see an error about 'Less secure apps'"
**Solution:** This is outdated. Gmail no longer uses "Less secure apps" setting. Use App Passwords instead.

---

## ALTERNATIVE: Use a Different Email Service

If you continue to have issues with Gmail, you can use:

### Option 1: SendGrid (Recommended)
1. Sign up at https://sendgrid.com (free tier available)
2. Get your API key
3. Update .env:
   ```
   MAIL_SERVER=smtp.sendgrid.net
   MAIL_PORT=587
   MAIL_USERNAME=apikey
   MAIL_PASSWORD=SG.your_api_key_here
   ```

### Option 2: Mailgun
1. Sign up at https://www.mailgun.com (free tier available)
2. Get your SMTP credentials
3. Update .env with their SMTP details

### Option 3: AWS SES
1. Set up AWS account
2. Verify your email in SES
3. Get SMTP credentials
4. Update .env with AWS SMTP details

---

## EMAIL FEATURES IMPLEMENTED

The application sends emails for:
1. **Welcome Email** - Sent when a new user registers
2. **Application Confirmation** - Sent when an applicant submits their grant application
3. **Application Approved** - Sent when admin approves an application
4. **Application Rejected** - Sent when admin rejects an application

All emails include:
- Professional HTML formatting
- Clear call-to-action
- Application details
- Next steps for the applicant

---

## QUICK REFERENCE

| Step | Action |
|------|--------|
| 1 | Go to https://myaccount.google.com/security |
| 2 | Enable 2-Step Verification |
| 3 | Find "App passwords" (appears after 2FA enabled) |
| 4 | Select Mail + Windows Computer |
| 5 | Copy the 16-character password |
| 6 | Update .env: `MAIL_PASSWORD=xxxx xxxx xxxx xxxx` |
| 7 | Restart Flask application |
| 8 | Test by creating new account |
