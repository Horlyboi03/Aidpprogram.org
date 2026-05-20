# 🚀 AIDP Deployment Guide - Step by Step

## ✅ Pre-Deployment Checklist
Your application is ready to deploy! All necessary files are in place:
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Gunicorn configuration
- ✅ `.gitignore` - Security files excluded
- ✅ `config.py` - Production-ready configuration

---

## 📋 What You'll Need
1. **Domain name** (you already have this!)
2. **GitHub account** (to push your code)
3. **Supabase account** (free database)
4. **Render account** (free or $7/month hosting)

---

## STEP 1: Push Code to GitHub

### 1.1 Initialize Git (if not already done)
Open PowerShell in your project folder:
```powershell
cd "C:\Users\HP\Desktop\new ai"
git init
```

### 1.2 Add all files
```powershell
git add .
```

### 1.3 Commit your code
```powershell
git commit -m "Initial commit - AIDP ready for deployment"
```

### 1.4 Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `aidp-grant-system` (or any name you prefer)
3. Make it **Private** (recommended for security)
4. Click "Create repository"

### 1.5 Push to GitHub
Copy the commands from GitHub (they'll look like this):
```powershell
git remote add origin https://github.com/YOUR-USERNAME/aidp-grant-system.git
git branch -M main
git push -u origin main
```

---

## STEP 2: Set Up Supabase Database (FREE)

### 2.1 Create Supabase Account
1. Go to https://supabase.com
2. Click "Start your project"
3. Sign up with GitHub (easiest)

### 2.2 Create New Project
1. Click "New Project"
2. **Organization**: Create new or use existing
3. **Project Name**: `aidp-database`
4. **Database Password**: Create a STRONG password (save it!)
5. **Region**: Choose closest to your users
6. Click "Create new project" (takes 2-3 minutes)

### 2.3 Get Database Connection String
1. Once project is ready, click "Connect"
2. Select "URI" tab
3. Copy the connection string (looks like):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```
4. **SAVE THIS** - you'll need it for Render!

---

## STEP 3: Deploy to Render

### 3.1 Create Render Account
1. Go to https://render.com
2. Click "Get Started"
3. Sign up with GitHub (easiest - auto-connects your repos)

### 3.2 Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `aidp-grant-system`
3. Click "Connect"

### 3.3 Configure Web Service
Fill in these settings:

**Basic Settings:**
- **Name**: `aidp-grant-system` (or your preferred name)
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: (leave blank)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn run:app`

**Instance Type:**
- **Free** (sleeps after 15 min inactivity) OR
- **Starter - $7/month** (always on, recommended for production)

### 3.4 Add Environment Variables
Click "Advanced" → "Add Environment Variable"

Add these **CRITICAL** variables:

```
SECRET_KEY = your-super-secret-random-key-here-change-this
DATABASE_URL = postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres
ADMIN_EMAIL = maryygeorge193@gmail.com
ADMIN_PASSWORD = Horlyboi1607
ADMIN_NAME = Mary George
MAIL_SERVER = smtp.gmail.com
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = maryygeorge193@gmail.com
MAIL_PASSWORD = bbugpxegjppzyjja
MAIL_DEFAULT_SENDER = maryygeorge193@gmail.com
```

**IMPORTANT**: 
- Replace `DATABASE_URL` with your Supabase connection string from Step 2.3
- Generate a strong `SECRET_KEY` (use: https://randomkeygen.com/)

### 3.5 Deploy!
1. Click "Create Web Service"
2. Render will start building (takes 3-5 minutes)
3. Watch the logs - you'll see:
   - Installing dependencies
   - Starting Gunicorn
   - "Application startup complete"

---

## STEP 4: Initialize Database

### 4.1 Access Render Shell
1. In Render dashboard, click your service
2. Click "Shell" tab (top right)
3. Run these commands:

```bash
python
```

Then in Python shell:
```python
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print("Database tables created!")
exit()
```

### 4.2 Create Admin User
Still in Render Shell:
```bash
python
```

```python
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    admin = User(
        email='maryygeorge193@gmail.com',
        name='Mary George',
        password_hash=generate_password_hash('Horlyboi1607'),
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()
    print("Admin user created!")
exit()
```

---

## STEP 5: Connect Your Domain

### 5.1 Get Render URL
Your app is now live at: `https://aidp-grant-system.onrender.com`

### 5.2 Add Custom Domain
1. In Render dashboard, click "Settings"
2. Scroll to "Custom Domains"
3. Click "Add Custom Domain"
4. Enter your domain: `yourdomain.com`

### 5.3 Update DNS Settings
Go to your domain registrar (where you bought the domain):

**Add these DNS records:**

For root domain (`yourdomain.com`):
```
Type: A
Name: @
Value: [IP from Render]
TTL: 3600
```

For www subdomain (`www.yourdomain.com`):
```
Type: CNAME
Name: www
Value: aidp-grant-system.onrender.com
TTL: 3600
```

**DNS propagation takes 5-60 minutes**

---

## STEP 6: Test Your Live Site

### 6.1 Visit Your Site
Go to: `https://yourdomain.com` (or Render URL)

### 6.2 Test These Features:
- ✅ Homepage loads
- ✅ Register new user
- ✅ Login as user
- ✅ Submit application
- ✅ Login as admin: maryygeorge193@gmail.com / Horlyboi1607
- ✅ View applications
- ✅ Chat system works
- ✅ Email notifications work

---

## 🎉 YOU'RE LIVE!

Your AIDP grant management system is now deployed and accessible worldwide!

### Important URLs:
- **Live Site**: https://yourdomain.com
- **Admin Login**: https://yourdomain.com/login
- **Render Dashboard**: https://dashboard.render.com
- **Supabase Dashboard**: https://app.supabase.com

### Costs:
- **Supabase**: FREE forever (500MB database)
- **Render Free**: FREE (sleeps after 15 min)
- **Render Starter**: $7/month (always on, recommended)

---

## 🔧 Troubleshooting

### Issue: "Application failed to start"
**Solution**: Check Render logs for errors. Usually missing environment variables.

### Issue: "Database connection failed"
**Solution**: Verify DATABASE_URL is correct in Render environment variables.

### Issue: "Admin can't login"
**Solution**: Re-run Step 4.2 to create admin user.

### Issue: "Domain not working"
**Solution**: Wait 30-60 minutes for DNS propagation. Check DNS settings.

### Issue: "Emails not sending"
**Solution**: Verify MAIL_USERNAME and MAIL_PASSWORD in environment variables.

---

## 📱 Next Steps After Deployment

1. **Test thoroughly** - Try all features
2. **Monitor logs** - Check Render logs for errors
3. **Set up backups** - Supabase has automatic backups
4. **Share your link** - Start accepting applications!
5. **Monitor usage** - Check Supabase and Render dashboards

---

## 🆘 Need Help?

If you encounter issues:
1. Check Render logs (Logs tab in dashboard)
2. Check Supabase logs (Logs section)
3. Verify all environment variables are set correctly
4. Make sure database tables were created (Step 4.1)

---

**Deployment Date**: May 20, 2026
**Version**: 1.0.0
**Status**: Production Ready ✅
