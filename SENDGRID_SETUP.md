# SendGrid Email Setup (Free Alternative to Gmail)

Since Gmail is blocking SMTP access, we'll use SendGrid instead. It's free for up to 100 emails per day.

## Step 1: Create SendGrid Account

1. Go to: https://sendgrid.com
2. Click "Sign Up Free"
3. Fill in your details:
   - Email: maryygeorge193@gmail.com
   - Password: Create a new password
   - Company: AIDP
4. Verify your email
5. Complete the setup wizard

## Step 2: Get Your API Key

1. Log in to SendGrid
2. Go to: Settings → API Keys
3. Click "Create API Key"
4. Name it: "AIDP Application"
5. Select "Full Access"
6. Click "Create & View"
7. Copy the API key (it starts with `SG.`)

## Step 3: Update .env File

Replace the `MAIL_PASSWORD` with your SendGrid API key:

```
MAIL_PASSWORD=SG.your_api_key_here
```

Example:
```
MAIL_PASSWORD=SG.1234567890abcdefghijklmnopqrstuvwxyz
```

## Step 4: Verify Sender Email

1. In SendGrid, go to: Settings → Sender Authentication
2. Click "Verify a Single Sender"
3. Enter your email: maryygeorge193@gmail.com
4. Click "Create"
5. Check your email for verification link
6. Click the link to verify

## Step 5: Test It

1. Restart the application
2. Run: `python test_email.py`
3. Check if you receive the test email

## Step 6: Update Email Sender

In the application, emails will now come from maryygeorge193@gmail.com via SendGrid.

---

## Why SendGrid?

✓ Free tier: 100 emails/day
✓ No complex authentication
✓ Reliable delivery
✓ Easy to set up
✓ Professional email service

---

## Troubleshooting

### "Still not receiving emails"
- Make sure you verified your sender email in SendGrid
- Check spam folder
- Wait a few minutes for SendGrid to process

### "API key not working"
- Make sure you copied the full API key (starts with SG.)
- No spaces or extra characters
- Restart the application after updating .env

### "Want to go back to Gmail?"
- Enable "Less secure app access" at: https://myaccount.google.com/lesssecureapps
- Use your Gmail password in MAIL_PASSWORD
- Change MAIL_SERVER back to smtp.gmail.com
