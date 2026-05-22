# Email Configuration Check

## Current .env Settings:
```
EMAIL_ENABLED=true
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=maryygeorge193@gmail.com
MAIL_PASSWORD=bbugpxegjppzyjja
MAIL_DEFAULT_SENDER=maryygeorge193@gmail.com
```

## CRITICAL: Render Environment Variables

You MUST set these in Render Dashboard:

1. Go to: https://dashboard.render.com
2. Select your service
3. Go to "Environment" tab
4. Add these variables:

```
EMAIL_ENABLED=true
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=maryygeorge193@gmail.com
MAIL_PASSWORD=bbugpxegjppzyjja
MAIL_DEFAULT_SENDER=maryygeorge193@gmail.com
```

## Why Emails Don't Work:

The `.env` file is NOT deployed to Render. It's only for local development.

On Render, you must set environment variables in the dashboard.

## Steps to Fix:

1. Open Render dashboard
2. Click your service
3. Click "Environment" in left menu
4. Click "Add Environment Variable"
5. Add each variable above
6. Click "Save Changes"
7. Render will redeploy automatically

## Test After Setting Variables:

1. Wait 2-3 minutes for redeploy
2. Submit a test application
3. Check applicant email
4. Check Render logs for: `[EMAIL] Application confirmation sent`
