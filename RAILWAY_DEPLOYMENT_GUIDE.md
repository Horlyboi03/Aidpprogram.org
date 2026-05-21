# 🚂 Railway Deployment Guide - Complete Setup

## ✅ What You'll Get
- Your app live at: **https://aidpprogram.org** (your custom domain)
- Automatic HTTPS/SSL certificate
- Free hosting (500 hours/month + $5 credit)
- Works with your Supabase database
- Automatic deployments from GitHub
- Always-on (no sleeping with free credit)

---

## 📋 Prerequisites
- ✅ GitHub account with your code pushed
- ✅ Domain name: aidpprogram.org (you have this)
- ✅ Supabase database (you have this)
- ✅ No credit card required to start!

---

## STEP 1: Create Railway Account

### 1.1 Sign Up
1. Go to: **https://railway.app**
2. Click **"Login"**
3. Click **"Login with GitHub"**
4. Authorize Railway to access your GitHub account
5. You're in! No credit card needed.

---

## STEP 2: Deploy Your App from GitHub

### 2.1 Create New Project
1. Click **"New Project"** (big button in the center)
2. Select **"Deploy from GitHub repo"**
3. You'll see a list of your repositories
4. Find and click: **Horlyboi03/Aidpprogram.org**
5. Railway will automatically detect it's a Python app
6. Click **"Deploy Now"**

### 2.2 Wait for Initial Deployment
- Railway will start deploying (takes 2-3 minutes)
- You'll see logs showing the build process
- **It will fail first** - that's okay! We need to add environment variables

---

## STEP 3: Add Environment Variables

### 3.1 Open Variables Tab
1. Click on your deployed service (the card showing your app)
2. Click the **"Variables"** tab at the top
3. You'll see an empty variables section

### 3.2 Add All 11 Variables
Click **"New Variable"** and add each of these:

**Variable 1:**
```
Name: SECRET_KEY
Value: aidp-super-secret-key-change-in-production-12345
```

**Variable 2:**
```
Name: DATABASE_URL
Value: postgresql://postgres:Salamiolawale1607!@db.rumotzspnrzsbugflimb.supabase.co:5432/postgres
```

**Variable 3:**
```
Name: ADMIN_EMAIL
Value: maryygeorge193@gmail.com
```

**Variable 4:**
```
Name: ADMIN_PASSWORD
Value: Horlyboi1607
```

**Variable 5:**
```
Name: ADMIN_NAME
Value: Mary George
```

**Variable 6:**
```
Name: MAIL_SERVER
Value: smtp.gmail.com
```

**Variable 7:**
```
Name: MAIL_PORT
Value: 587
```

**Variable 8:**
```
Name: MAIL_USE_TLS
Value: True
```

**Variable 9:**
```
Name: MAIL_USERNAME
Value: maryygeorge193@gmail.com
```

**Variable 10:**
```
Name: MAIL_PASSWORD
Value: bbugpxegjppzyjja
```

**Variable 11:**
```
Name: MAIL_DEFAULT_SENDER
Value: maryygeorge193@gmail.com
```

### 3.3 Redeploy
1. After adding all variables, Railway will automatically redeploy
2. Go to the **"Deployments"** tab to watch the logs
3. Wait 2-3 minutes for deployment to complete
4. You should see: "Application startup complete" ✅

---

## STEP 4: Get Your Railway URL

### 4.1 Generate Public URL
1. Click on **"Settings"** tab
2. Scroll down to **"Networking"** section
3. Click **"Generate Domain"**
4. Railway will give you a URL like: `aidpprogram-production.up.railway.app`
5. Click on the URL to test your app
6. You should see your homepage! 🎉

---

## STEP 5: Connect Your Custom Domain (aidpprogram.org)

### 5.1 Add Custom Domain in Railway
1. Still in **"Settings"** → **"Networking"**
2. Under "Custom Domains", click **"Custom Domain"**
3. Enter: `aidpprogram.org`
4. Click **"Add"**
5. Railway will show you DNS records to add

### 5.2 Railway Will Show You These Records
Railway will display something like:

```
Add these DNS records to your domain:

Type: CNAME
Name: aidpprogram.org (or @)
Value: aidpprogram-production.up.railway.app

Type: CNAME
Name: www
Value: aidpprogram-production.up.railway.app
```

**Copy these values** - you'll need them in the next step.

---

## STEP 6: Update DNS at Your Domain Registrar

### 6.1 Go to Your Domain Provider
Go to where you bought **aidpprogram.org** (e.g., Namecheap, GoDaddy, Google Domains, etc.)

### 6.2 Find DNS Settings
Look for:
- "DNS Management"
- "DNS Settings"
- "Manage DNS"
- "Advanced DNS"

### 6.3 Add DNS Records

**For Root Domain (aidpprogram.org):**

If your registrar supports CNAME for root:
```
Type: CNAME
Host: @ (or leave blank, or aidpprogram.org)
Value: aidpprogram-production.up.railway.app
TTL: 3600 (or Automatic)
```

If your registrar requires A record for root:
```
Type: A
Host: @
Value: [Get IP from Railway - they'll provide it]
TTL: 3600
```

**For WWW Subdomain:**
```
Type: CNAME
Host: www
Value: aidpprogram-production.up.railway.app
TTL: 3600
```

### 6.4 Save DNS Changes
1. Click **"Save"** or **"Add Record"**
2. Wait 5-60 minutes for DNS propagation (usually 10-15 minutes)

---

## STEP 7: Verify SSL Certificate

### 7.1 Wait for SSL
1. After DNS propagates, go back to Railway
2. In **Settings** → **Networking** → **Custom Domains**
3. You'll see your domain with a status
4. Wait for SSL certificate to be issued (automatic, takes 5-10 minutes)
5. Status will change to "Active" with a green checkmark ✅

### 7.2 Test Your Domain
1. Open browser
2. Go to: **https://aidpprogram.org**
3. Your site should load with HTTPS! 🎉
4. Also test: **https://www.aidpprogram.org**

---

## STEP 8: Test Your Application

### 8.1 Test Homepage
Visit: https://aidpprogram.org
- Should see your homepage
- All images and styles should load

### 8.2 Test User Registration
1. Click "Register"
2. Create a test user account
3. Should receive confirmation

### 8.3 Test Admin Login
1. Go to: https://aidpprogram.org/login
2. Login with:
   - Email: maryygeorge193@gmail.com
   - Password: Horlyboi1607
3. Should see admin dashboard

### 8.4 Test Application Submission
1. Login as regular user
2. Submit a test application
3. Check if it appears in admin dashboard

### 8.5 Test Chat System
1. Send a message as user
2. Reply as admin
3. Verify real-time updates work

---

## 🎉 YOU'RE LIVE!

Your application is now deployed and accessible at:
- **Main URL**: https://aidpprogram.org
- **WWW URL**: https://www.aidpprogram.org
- **Admin Login**: https://aidpprogram.org/login

---

## 💰 Cost Breakdown

**Railway Free Tier:**
- 500 execution hours/month (FREE)
- $5 usage credit/month (FREE)
- This covers ~20-30 days of always-on hosting
- Custom domain: FREE
- SSL certificate: FREE
- Automatic deployments: FREE

**Supabase Database:**
- 500MB storage: FREE
- Unlimited API requests: FREE
- Daily backups: FREE

**Total Monthly Cost: $0** (on free tier)

**If you exceed free tier:**
- Railway charges ~$5-10/month for typical usage
- Still very affordable!

---

## 🔄 Automatic Deployments

Every time you push to GitHub:
1. Railway automatically detects the change
2. Builds and deploys the new version
3. Your site updates automatically
4. Zero downtime deployments

To push updates:
```powershell
cd "C:\Users\HP\Desktop\new ai"
git add .
git commit -m "Your update message"
git push origin main
```

Railway will deploy automatically in 2-3 minutes!

---

## 📊 Monitoring Your App

### View Logs
1. Go to Railway dashboard
2. Click on your service
3. Click **"Deployments"** tab
4. Click on latest deployment
5. See real-time logs

### Check Usage
1. Click **"Usage"** tab
2. See execution hours used
3. Monitor credit usage
4. Get alerts before limits

---

## 🔧 Troubleshooting

### Issue: "Domain not working"
**Solution**: 
- Wait 30-60 minutes for DNS propagation
- Check DNS records are correct
- Use https://dnschecker.org to verify propagation

### Issue: "SSL certificate pending"
**Solution**:
- Wait 10-15 minutes after DNS propagates
- Railway automatically issues SSL
- Check domain status in Railway dashboard

### Issue: "Application error"
**Solution**:
- Check deployment logs in Railway
- Verify all 11 environment variables are set
- Check DATABASE_URL is correct

### Issue: "Database connection failed"
**Solution**:
- Verify DATABASE_URL in Railway variables
- Test connection in Supabase dashboard
- Make sure Supabase project is active

---

## 🆘 Need Help?

### Railway Support
- Documentation: https://docs.railway.app
- Discord: https://discord.gg/railway
- Twitter: @Railway

### Check These First
1. All environment variables set correctly
2. DNS records added at domain registrar
3. Supabase database is active
4. Latest code pushed to GitHub

---

## 🎯 Next Steps After Deployment

1. **Test thoroughly** - Try all features
2. **Monitor logs** - Check for any errors
3. **Share your link** - Start accepting applications!
4. **Set up monitoring** - Use Railway's built-in monitoring
5. **Plan for scaling** - Monitor usage and upgrade if needed

---

## 📱 Mobile Access

Your site is fully responsive and works on:
- ✅ Desktop browsers
- ✅ Mobile phones (iOS/Android)
- ✅ Tablets
- ✅ All modern browsers

---

## 🔐 Security Features

Your deployment includes:
- ✅ HTTPS/SSL encryption (automatic)
- ✅ Secure database connection
- ✅ Environment variables (not in code)
- ✅ Password hashing
- ✅ CSRF protection
- ✅ Secure session management

---

## 📈 Scaling Options

**When you outgrow free tier:**

**Option 1: Stay on Railway**
- Add credit card
- Pay-as-you-go: ~$5-10/month
- Automatic scaling

**Option 2: Upgrade to Pro**
- Railway Pro: $20/month
- More resources
- Priority support

**Option 3: Move to DigitalOcean**
- $5-12/month
- More control
- Managed database option

---

**Deployment Date**: May 21, 2026
**Platform**: Railway
**Domain**: aidpprogram.org
**Database**: Supabase (PostgreSQL)
**Status**: Production Ready ✅

---

**Your app will be live at https://aidpprogram.org in about 15-20 minutes!**
