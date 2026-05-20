# 🚀 DEPLOY WITH SUPABASE + RENDER

## Why Supabase?
- ✅ **FREE** PostgreSQL database (500MB storage, unlimited API requests)
- ✅ No credit card required
- ✅ Auto-backups
- ✅ Easy to use dashboard
- ✅ Never sleeps (unlike Render free database)

---

## STEP 1: CREATE SUPABASE ACCOUNT & DATABASE (5 minutes)

### 1.1 Sign Up
1. Go to **https://supabase.com**
2. Click "Start your project"
3. Sign up with GitHub (easiest) or email
4. Verify your email if needed

### 1.2 Create New Project
1. Click "New Project"
2. Fill in:
   - **Name**: `aidp-grant-system`
   - **Database Password**: Create a strong password (SAVE THIS!)
   - **Region**: Choose closest to you (e.g., US East, Europe West)
   - **Pricing Plan**: **Free** (perfect for your needs)
3. Click "Create new project"
4. Wait 2-3 minutes for setup

### 1.3 Get Database Connection String
1. In your project dashboard, click **"Settings"** (gear icon, bottom left)
2. Click **"Database"** in the left menu
3. Scroll to **"Connection string"** section
4. Select **"URI"** tab
5. Copy the connection string (looks like: `postgresql://postgres:[YOUR-PASSWORD]@...`)
6. **IMPORTANT**: Replace `[YOUR-PASSWORD]` with the password you created in step 1.2
7. Save this complete URL - you'll need it!

Example:
```
postgresql://postgres:YourPassword123@db.abcdefghijk.supabase.co:5432/postgres
```

---

## STEP 2: UPLOAD CODE TO GITHUB (5 minutes)

### 2.1 Create GitHub Account
1. Go to **https://github.com**
2. Sign up (if you don't have an account)
3. Verify email

### 2.2 Create Repository
1. Click **"+"** (top right) → "New repository"
2. Name: `aidp-grant-system`
3. Make it **Private**
4. Don't check any boxes
5. Click "Create repository"

### 2.3 Push Your Code
Open PowerShell in: `C:\Users\HP\Desktop\new ai`

```powershell
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - AIDP with Supabase"

# Add remote (replace YOUR-USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/aidp-grant-system.git

# Push
git branch -M main
git push -u origin main
```

**If it asks for credentials:**
- Username: your GitHub username
- Password: Create a Personal Access Token:
  - GitHub → Settings → Developer settings → Personal access tokens → Generate new token (classic)
  - Check "repo"
  - Copy token and use as password

---

## STEP 3: DEPLOY TO RENDER (5 minutes)

### 3.1 Create Render Account
1. Go to **https://render.com**
2. Click "Get Started"
3. Sign in with GitHub (easiest)
4. Authorize Render

### 3.2 Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Click "Connect a repository"
3. Find and select `aidp-grant-system`
4. Click "Connect"

### 3.3 Configure Service
Fill in these settings:

- **Name**: `aidp-grant-system` (or your domain name)
- **Region**: Same as Supabase (or closest)
- **Branch**: `main`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn run:app`
- **Instance Type**: **Free** (for testing) or **Starter $7/month** (for production)

### 3.4 Add Environment Variables
Scroll down to "Environment Variables" and add these:

```
Key: SECRET_KEY
Value: aidp-super-secret-key-2026-make-this-very-long-and-random-change-it

Key: DATABASE_URL
Value: [Paste your Supabase connection string from Step 1.3]

Key: MAIL_USERNAME
Value: maryygeorge193@gmail.com

Key: MAIL_PASSWORD
Value: bbugpxegjppzyjja

Key: MAIL_SERVER
Value: smtp.gmail.com

Key: MAIL_PORT
Value: 587

Key: MAIL_USE_TLS
Value: True

Key: FLASK_ENV
Value: production
```

### 3.5 Deploy!
1. Click **"Create Web Service"**
2. Wait 5-10 minutes
3. Watch the logs - you'll see packages installing
4. When you see "Deploy live" - you're online!
5. You'll get a URL like: `https://aidp-grant-system.onrender.com`

---

## STEP 4: INITIALIZE DATABASE (3 minutes)

### 4.1 Create Tables
1. In Render dashboard, go to your web service
2. Click **"Shell"** tab (top menu)
3. Wait for shell to connect
4. Type: `python` and press Enter
5. Copy and paste this:

```python
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print("✓ Database tables created!")
exit()
```

### 4.2 Verify in Supabase
1. Go back to Supabase dashboard
2. Click **"Table Editor"** (left menu)
3. You should see your tables: `users`, `applications`, `messages`, `admin_notifications`

---

## STEP 5: TEST YOUR WEBSITE (2 minutes)

1. Click the URL at top of Render dashboard
2. Your website should load!
3. Test:
   - ✅ Homepage loads
   - ✅ Register a new account
   - ✅ Login works
   - ✅ Try submitting an application

---

## STEP 6: CREATE ADMIN ACCOUNT (2 minutes)

### Option A: Register Then Upgrade (Easiest)
1. Register on your website with: `maryygeorge193@gmail.com`
2. Then in Render Shell:

```python
from app import create_app, db
from app.models import User
app = create_app()
with app.app_context():
    user = User.query.filter_by(email='maryygeorge193@gmail.com').first()
    user.role = 'admin'
    db.session.commit()
    print("✓ Admin role set!")
exit()
```

### Option B: Create Admin Directly
In Render Shell:

```python
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    admin = User(
        name='Mary George',
        email='maryygeorge193@gmail.com',
        password_hash=generate_password_hash('Horlyboi1607'),
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()
    print("✓ Admin created!")
exit()
```

---

## STEP 7: CONNECT YOUR DOMAIN (10 minutes)

### 7.1 In Render Dashboard
1. Go to your web service settings
2. Scroll to **"Custom Domains"**
3. Click **"Add Custom Domain"**
4. Enter your domain (e.g., `www.yourdomain.com`)
5. Render will show DNS records to add

### 7.2 In Your Domain Provider
Add these DNS records (values from Render):

**For www.yourdomain.com:**
```
Type: CNAME
Host: www
Value: aidp-grant-system.onrender.com
TTL: Automatic
```

**For yourdomain.com (root):**
```
Type: A
Host: @
Value: [IP address from Render]
TTL: Automatic
```

### 7.3 Wait for DNS
- Usually takes 10 minutes to 2 hours
- Sometimes up to 24-48 hours
- Check: https://www.whatsmydns.net

---

## 🎉 YOU'RE LIVE!

Your website is now online with:
- ✅ Free Supabase PostgreSQL database
- ✅ Render hosting (free or $7/month)
- ✅ Your custom domain
- ✅ Automatic HTTPS

---

## UPDATING YOUR WEBSITE

When you make changes:

```powershell
git add .
git commit -m "Description of changes"
git push
```

Render automatically redeploys! (takes 2-5 minutes)

---

## MONITORING

### Check Logs
- **Render**: Dashboard → Your service → "Logs" tab
- **Supabase**: Dashboard → "Logs" section

### Database Management
- **Supabase Dashboard**: View/edit data directly
- **Table Editor**: See all your data
- **SQL Editor**: Run custom queries

### Backups
- Supabase automatically backs up your database
- Free tier: 7 days of backups
- Paid tier: 30 days of backups

---

## COSTS BREAKDOWN

### Free Tier (Perfect for Testing)
- **Supabase Database**: FREE (500MB, unlimited requests)
- **Render Web Service**: FREE (sleeps after 15 min inactivity)
- **Domain**: Already paid
- **Total**: $0/month

### Production Tier (Recommended)
- **Supabase Database**: FREE (still free!)
- **Render Web Service**: $7/month (always on, no sleep)
- **Domain**: Already paid
- **Total**: $7/month

### If You Need More
- **Supabase Pro**: $25/month (8GB database, more features)
- **Render Pro**: $25/month (more resources)

---

## ADVANTAGES OF SUPABASE

✅ **Free forever** (500MB is plenty for your app)
✅ **Never sleeps** (unlike Render free database)
✅ **Auto backups** included
✅ **Easy dashboard** to view/edit data
✅ **Real-time features** (if you need them later)
✅ **No credit card** required
✅ **Great documentation**

---

## TROUBLESHOOTING

### "Application Error" on Render
- Check Render logs
- Verify DATABASE_URL is correct
- Make sure you ran `db.create_all()`

### Database connection failed
- Check Supabase password is correct in DATABASE_URL
- Verify Supabase project is active
- Check connection string format

### Can't see tables in Supabase
- Make sure you ran `db.create_all()` in Step 4
- Refresh Supabase dashboard
- Check Render logs for errors

### Domain not working
- Wait longer (DNS takes time)
- Verify DNS records are correct
- Clear browser cache
- Try incognito/private mode

---

## SUPABASE DASHBOARD FEATURES

### Table Editor
- View all your data
- Edit records directly
- Add/delete rows
- Export data

### SQL Editor
- Run custom SQL queries
- Create views
- Manage indexes

### Database Settings
- View connection info
- Manage extensions
- Configure pooling

### Logs
- See all database queries
- Monitor performance
- Debug issues

---

## SECURITY CHECKLIST

Before going live:
- ✅ Change SECRET_KEY to something random
- ✅ Use strong Supabase password
- ✅ Keep DATABASE_URL secret
- ✅ Enable 2FA on GitHub
- ✅ Enable 2FA on Supabase
- ✅ Enable 2FA on Render
- ✅ Review Supabase security settings
- ✅ Set up regular backups

---

## NEXT STEPS

1. ✅ Test everything thoroughly
2. ✅ Share your domain with users
3. ✅ Monitor Supabase dashboard
4. ✅ Check Render logs regularly
5. ✅ Consider upgrading Render to paid tier for production
6. ✅ Set up monitoring/alerts
7. ✅ Add Google Analytics (optional)

---

## USEFUL LINKS

- **Supabase Dashboard**: https://app.supabase.com
- **Render Dashboard**: https://dashboard.render.com
- **Supabase Docs**: https://supabase.com/docs
- **Render Docs**: https://render.com/docs

---

## NEED HELP?

### Supabase Support
- Discord: https://discord.supabase.com
- Docs: https://supabase.com/docs
- Email: support@supabase.io

### Render Support
- Docs: https://render.com/docs
- Community: https://community.render.com
- Email: support@render.com

---

**Congratulations! Your AIDP system is now live with Supabase + Render! 🎉**

**Total Cost: $0-7/month (vs $14/month with Render database)**
