# ✅ AIDP Deployment Checklist

## Before You Start
- [ ] You have your domain name ready
- [ ] You have a GitHub account
- [ ] You have a credit/debit card (for Render Starter plan - optional but recommended)
- [ ] Your local application is working correctly

---

## Phase 1: GitHub Setup (10 minutes)
- [ ] Open PowerShell in project folder: `cd "C:\Users\HP\Desktop\new ai"`
- [ ] Initialize Git: `git init`
- [ ] Add files: `git add .`
- [ ] Commit: `git commit -m "Initial commit - AIDP ready for deployment"`
- [ ] Create GitHub repository at https://github.com/new
- [ ] Name it: `aidp-grant-system` (or your choice)
- [ ] Set to Private
- [ ] Push code to GitHub using commands provided
- [ ] Verify code is visible on GitHub

---

## Phase 2: Supabase Database (5 minutes)
- [ ] Go to https://supabase.com
- [ ] Sign up with GitHub
- [ ] Create new project: "aidp-database"
- [ ] Choose region closest to your users
- [ ] Create STRONG database password
- [ ] **SAVE PASSWORD** in safe place
- [ ] Wait for project to be ready (2-3 minutes)
- [ ] Click "Connect" → "URI" tab
- [ ] Copy connection string
- [ ] **SAVE CONNECTION STRING** - you'll need it!

---

## Phase 3: Render Deployment (15 minutes)
- [ ] Go to https://render.com
- [ ] Sign up with GitHub
- [ ] Click "New +" → "Web Service"
- [ ] Connect your `aidp-grant-system` repository
- [ ] Configure settings:
  - [ ] Name: `aidp-grant-system`
  - [ ] Runtime: Python 3
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `gunicorn run:app`
  - [ ] Instance Type: **Starter ($7/month)** recommended
- [ ] Click "Advanced" → Add Environment Variables
- [ ] Add all 10 environment variables (see QUICK_DEPLOY_COMMANDS.txt)
  - [ ] SECRET_KEY (generate at randomkeygen.com)
  - [ ] DATABASE_URL (from Supabase)
  - [ ] ADMIN_EMAIL
  - [ ] ADMIN_PASSWORD
  - [ ] ADMIN_NAME
  - [ ] MAIL_SERVER
  - [ ] MAIL_PORT
  - [ ] MAIL_USE_TLS
  - [ ] MAIL_USERNAME
  - [ ] MAIL_PASSWORD
  - [ ] MAIL_DEFAULT_SENDER
- [ ] Click "Create Web Service"
- [ ] Wait for deployment (3-5 minutes)
- [ ] Check logs - should see "Application startup complete"

---

## Phase 4: Database Initialization (5 minutes)
- [ ] In Render dashboard, click "Shell" tab
- [ ] Run: `python`
- [ ] Copy and paste database creation commands (from QUICK_DEPLOY_COMMANDS.txt)
- [ ] Verify: "Database tables created!" message
- [ ] Exit: `exit()`
- [ ] Run: `python` again
- [ ] Copy and paste admin user creation commands
- [ ] Verify: "Admin user created!" message
- [ ] Exit: `exit()`

---

## Phase 5: Domain Connection (30-60 minutes)
- [ ] Copy your Render URL: `https://aidp-grant-system.onrender.com`
- [ ] Test it - your site should be live!
- [ ] In Render: Settings → Custom Domains
- [ ] Add your domain name
- [ ] Go to your domain registrar (where you bought domain)
- [ ] Find DNS settings
- [ ] Add A record: @ → [Render IP]
- [ ] Add CNAME record: www → your-app.onrender.com
- [ ] Save DNS changes
- [ ] Wait 30-60 minutes for DNS propagation
- [ ] Test your domain: `https://yourdomain.com`

---

## Phase 6: Testing (10 minutes)
- [ ] Visit your live site
- [ ] Test homepage loads correctly
- [ ] Register a new test user
- [ ] Login as test user
- [ ] Submit a test application
- [ ] Logout
- [ ] Login as admin: maryygeorge193@gmail.com / Horlyboi1607
- [ ] View applications - test application should be there
- [ ] Test chat system
- [ ] Test email notifications
- [ ] Test on mobile device
- [ ] Test social media links in footer

---

## Phase 7: Go Live! 🎉
- [ ] Share your website URL with applicants
- [ ] Post on social media (Instagram/Facebook)
- [ ] Monitor Render logs for any errors
- [ ] Check Supabase dashboard for database usage
- [ ] Celebrate! Your application is live! 🚀

---

## Important Information to Save

### Your Live URLs:
- **Website**: https://yourdomain.com
- **Admin Login**: https://yourdomain.com/login
- **Render Dashboard**: https://dashboard.render.com
- **Supabase Dashboard**: https://app.supabase.com

### Admin Credentials:
- **Email**: maryygeorge193@gmail.com
- **Password**: Horlyboi1607

### Monthly Costs:
- **Supabase**: $0 (FREE forever)
- **Render**: $7/month (Starter plan - recommended)
- **Total**: $7/month

### Support Resources:
- **Render Docs**: https://render.com/docs
- **Supabase Docs**: https://supabase.com/docs
- **Flask Docs**: https://flask.palletsprojects.com/

---

## Troubleshooting

### ❌ Build Failed
**Check**: Render logs for specific error
**Fix**: Usually missing dependency in requirements.txt

### ❌ Database Connection Error
**Check**: DATABASE_URL environment variable
**Fix**: Verify connection string from Supabase is correct

### ❌ Admin Can't Login
**Check**: Did you run admin user creation commands?
**Fix**: Re-run Phase 4 admin creation commands

### ❌ Emails Not Sending
**Check**: MAIL_USERNAME and MAIL_PASSWORD environment variables
**Fix**: Verify Gmail app password is correct

### ❌ Domain Not Working
**Check**: DNS propagation (can take up to 60 minutes)
**Fix**: Wait longer, or check DNS settings are correct

---

## Post-Deployment Monitoring

### Daily:
- [ ] Check for new applications
- [ ] Respond to chat messages
- [ ] Monitor email notifications

### Weekly:
- [ ] Check Render logs for errors
- [ ] Review Supabase database usage
- [ ] Backup important data

### Monthly:
- [ ] Pay Render bill ($7)
- [ ] Review application statistics
- [ ] Update content if needed

---

**Ready to deploy? Start with Phase 1!**

Open `QUICK_DEPLOY_COMMANDS.txt` for copy-paste commands.
Open `DEPLOY_NOW.md` for detailed step-by-step instructions.
