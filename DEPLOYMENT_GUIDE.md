# 🚀 COMPLETE DEPLOYMENT GUIDE - AIDP Website

## Overview
This guide will walk you through buying a domain and deploying your AIDP grant management application to the internet.

---

## PART 1: BUYING A DOMAIN

### Option 1: Namecheap (Recommended - Affordable)
1. Go to **https://www.namecheap.com**
2. Search for your desired domain (e.g., "aidpgrants.com")
3. Add to cart and checkout
4. **Cost**: $8-15/year for .com domains
5. **Tip**: Look for first-year discounts

### Option 2: GoDaddy
1. Go to **https://www.godaddy.com**
2. Search and purchase domain
3. **Cost**: $10-20/year

### Option 3: Google Domains (Now Squarespace)
1. Go to **https://domains.google.com** (redirects to Squarespace)
2. Search and purchase
3. **Cost**: $12-20/year

### Domain Name Tips:
- Keep it short and memorable
- Use .com if possible (most trusted)
- Avoid hyphens and numbers
- Make it relevant to your service (e.g., aidpgrants.com, aidpfunding.com)

---

## PART 2: CHOOSING A HOSTING PLATFORM

### 🌟 RECOMMENDED: Render.com (Easiest for Flask)

#### Why Render?
- ✅ Free tier available
- ✅ Easy PostgreSQL database setup
- ✅ Automatic HTTPS/SSL
- ✅ Easy deployment from GitHub
- ✅ Good for Flask/Python apps
- ✅ Custom domain support

#### Pricing:
- **Free Tier**: Good for testing (sleeps after inactivity)
- **Starter**: $7/month (always on, better performance)
- **Database**: Free tier available, or $7/month for production

---

### Alternative Options:

#### 1. **Heroku** (Popular but more expensive)
- **Pros**: Very reliable, good documentation
- **Cons**: No free tier anymore, starts at $7/month
- **Best for**: Production apps with budget

#### 2. **PythonAnywhere** (Beginner-friendly)
- **Pros**: Easy setup, Python-focused
- **Cons**: Limited free tier, slower performance
- **Free Tier**: Yes, with limitations
- **Paid**: $5/month

#### 3. **Railway.app** (Modern alternative)
- **Pros**: Easy deployment, good free tier
- **Cons**: Newer platform
- **Free Tier**: $5 credit/month
- **Paid**: Pay as you go

#### 4. **DigitalOcean** (More control, more complex)
- **Pros**: Full server control, scalable
- **Cons**: Requires more technical knowledge
- **Cost**: $6/month minimum

---

## PART 3: DEPLOYMENT STEPS (Using Render.com)

### Step 1: Prepare Your Code

#### 1.1 Create requirements.txt
Create a file called `requirements.txt` in your project root:

```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.1
Flask-SocketIO==5.3.6
Flask-Mail==0.9.1
python-socketio==5.11.0
python-engineio==4.9.0
psycopg2-binary==2.9.9
gunicorn==21.2.0
python-dotenv==1.0.0
Werkzeug==3.0.1
email-validator==2.1.0
```

#### 1.2 Create Procfile
Create a file called `Procfile` (no extension) in your project root:

```
web: gunicorn run:app
```

#### 1.3 Update config.py for Production
Your config.py should detect production environment:

```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # Database - use PostgreSQL in production
    if os.environ.get('DATABASE_URL'):
        # Render/Heroku provides DATABASE_URL
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
    else:
        # Local development
        SQLALCHEMY_DATABASE_URI = 'sqlite:///aidp.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')
```

#### 1.4 Create .gitignore
Create `.gitignore` file:

```
__pycache__/
*.pyc
*.pyo
*.db
.env
venv/
env/
.vscode/
.idea/
*.log
instance/
```

### Step 2: Push to GitHub

#### 2.1 Create GitHub Account
- Go to **https://github.com**
- Sign up for free account

#### 2.2 Create New Repository
1. Click "New Repository"
2. Name it (e.g., "aidp-grant-system")
3. Make it **Private** (recommended for security)
4. Don't initialize with README (you already have code)

#### 2.3 Push Your Code
Open PowerShell in your project folder:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - AIDP Grant System"

# Add remote (replace with your GitHub URL)
git remote add origin https://github.com/YOUR-USERNAME/aidp-grant-system.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Render

#### 3.1 Create Render Account
1. Go to **https://render.com**
2. Sign up (use GitHub to sign in - easier)

#### 3.2 Create PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Name: `aidp-database`
3. Choose **Free** tier (or Starter for production)
4. Click "Create Database"
5. **IMPORTANT**: Copy the "Internal Database URL" - you'll need this

#### 3.3 Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `aidp-grant-system`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
   - **Plan**: Free (or Starter for production)

#### 3.4 Add Environment Variables
In the web service settings, add these environment variables:

```
SECRET_KEY = your-random-secret-key-here-make-it-long-and-random
DATABASE_URL = [paste the Internal Database URL from step 3.2]
MAIL_USERNAME = maryygeorge193@gmail.com
MAIL_PASSWORD = bbugpxegjppzyjja
FLASK_ENV = production
```

#### 3.5 Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for deployment
3. You'll get a URL like: `https://aidp-grant-system.onrender.com`

#### 3.6 Initialize Database
After first deployment, you need to create database tables:

1. Go to Render dashboard → Your web service
2. Click "Shell" tab
3. Run these commands:

```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
...     print("Database tables created!")
>>> exit()
```

### Step 4: Connect Your Domain

#### 4.1 In Render Dashboard
1. Go to your web service settings
2. Click "Custom Domains"
3. Click "Add Custom Domain"
4. Enter your domain (e.g., `www.aidpgrants.com`)
5. Render will show you DNS records to add

#### 4.2 In Your Domain Registrar (Namecheap/GoDaddy)
1. Log into your domain registrar
2. Go to DNS settings for your domain
3. Add the records Render provided:
   - **CNAME Record**: `www` → `aidp-grant-system.onrender.com`
   - **A Record**: `@` → Render's IP address

#### 4.3 Wait for DNS Propagation
- Takes 5 minutes to 48 hours (usually 1-2 hours)
- Check status at: https://www.whatsmydns.net

---

## PART 4: POST-DEPLOYMENT SETUP

### Create Admin Account
1. Visit your website
2. Register a new account with: maryygeorge193@gmail.com
3. Access database and set role to 'admin':

**Option A: Using Render Shell**
```bash
python
>>> from app import create_app, db
>>> from app.models import User
>>> app = create_app()
>>> with app.app_context():
...     user = User.query.filter_by(email='maryygeorge193@gmail.com').first()
...     user.role = 'admin'
...     db.session.commit()
...     print("Admin role set!")
>>> exit()
```

**Option B: Using SQL (in Render PostgreSQL dashboard)**
```sql
UPDATE users SET role = 'admin' WHERE email = 'maryygeorge193@gmail.com';
```

### Test Everything
- ✅ Homepage loads
- ✅ User registration works
- ✅ User login works
- ✅ Application submission works
- ✅ Admin login works
- ✅ Admin can view applications
- ✅ Chat system works
- ✅ Email notifications work

---

## PART 5: ONGOING MAINTENANCE

### Updating Your Website
When you make changes:

```bash
# Make your changes to code
# Then commit and push:
git add .
git commit -m "Description of changes"
git push

# Render will automatically redeploy!
```

### Monitoring
- Check Render dashboard for logs
- Monitor database usage
- Check email delivery

### Backups
- Render provides automatic database backups on paid plans
- Export database regularly for safety

---

## COST SUMMARY

### Minimal Budget (Testing/Small Scale)
- **Domain**: $10-15/year
- **Render Free Tier**: $0/month
- **Total**: ~$15/year

### Recommended (Production)
- **Domain**: $10-15/year
- **Render Web Service**: $7/month
- **Render Database**: $7/month
- **Total**: ~$170/year ($14/month)

### Professional (High Traffic)
- **Domain**: $15/year
- **Render Pro**: $25/month
- **Database**: $20/month
- **Total**: ~$555/year ($45/month)

---

## TROUBLESHOOTING

### Issue: "Application Error" on Render
**Solution**: Check logs in Render dashboard, usually missing environment variables

### Issue: Database connection fails
**Solution**: Make sure DATABASE_URL is set correctly in environment variables

### Issue: Static files not loading
**Solution**: Check that `app/static` folder is in your GitHub repo

### Issue: Emails not sending
**Solution**: Verify MAIL_USERNAME and MAIL_PASSWORD are set correctly

### Issue: Domain not connecting
**Solution**: Wait longer (DNS can take 24-48 hours), verify DNS records are correct

---

## SECURITY CHECKLIST

Before going live:
- ✅ Change SECRET_KEY to a strong random value
- ✅ Use environment variables for all secrets
- ✅ Enable HTTPS (Render does this automatically)
- ✅ Set strong admin password
- ✅ Review file upload security
- ✅ Test all forms for SQL injection protection (Flask-WTF handles this)
- ✅ Set up regular database backups

---

## NEED HELP?

### Render Documentation
- https://render.com/docs

### Flask Deployment Guide
- https://flask.palletsprojects.com/en/3.0.x/deploying/

### Contact Support
- Render: support@render.com
- Domain registrar support

---

## QUICK START CHECKLIST

- [ ] Buy domain from Namecheap/GoDaddy
- [ ] Create GitHub account and repository
- [ ] Create requirements.txt and Procfile
- [ ] Push code to GitHub
- [ ] Create Render account
- [ ] Create PostgreSQL database on Render
- [ ] Create web service on Render
- [ ] Add environment variables
- [ ] Deploy and initialize database
- [ ] Connect custom domain
- [ ] Create admin account
- [ ] Test all features
- [ ] Go live! 🎉

---

**Good luck with your deployment! Your AIDP grant management system is ready to help people worldwide.** 🌍
