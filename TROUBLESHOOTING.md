# 🔧 AIDP Deployment Troubleshooting Guide

## Common Issues and Solutions

---

## 🐛 Git Issues

### Issue: "git: command not found"
**Cause**: Git is not installed on your system

**Solution**:
1. Download Git from: https://git-scm.com/download/win
2. Run the installer
3. Use default settings
4. Restart PowerShell
5. Try again: `git --version`

---

### Issue: "fatal: not a git repository"
**Cause**: You're not in the correct folder

**Solution**:
```powershell
cd "C:\Users\HP\Desktop\new ai"
git init
```

---

### Issue: "Permission denied (publickey)"
**Cause**: GitHub SSH key not set up

**Solution**: Use HTTPS instead of SSH
```powershell
git remote set-url origin https://github.com/YOUR-USERNAME/aidp-grant-system.git
git push -u origin main
```

---

## 🗄️ Supabase Issues

### Issue: "Database connection failed"
**Cause**: Incorrect connection string

**Solution**:
1. Go to Supabase dashboard
2. Click your project
3. Click "Connect" button
4. Select "URI" tab
5. Copy the FULL connection string
6. Make sure you replaced `[YOUR-PASSWORD]` with your actual password
7. Update DATABASE_URL in Render environment variables

**Correct format**:
```
postgresql://postgres:YOUR_PASSWORD@db.xxxxx.supabase.co:5432/postgres
```

---

### Issue: "Could not connect to server"
**Cause**: Supabase project not ready or wrong region

**Solution**:
1. Wait 2-3 minutes for Supabase project to fully initialize
2. Check project status in Supabase dashboard (should be green)
3. Try connection string again

---

## 🚀 Render Issues

### Issue: "Build failed"
**Cause**: Missing dependencies or syntax error

**Solution**:
1. Check Render logs (Logs tab)
2. Look for the specific error message
3. Common fixes:
   - Verify `requirements.txt` has all dependencies
   - Check for typos in `Procfile`
   - Ensure `run.py` exists in root folder

---

### Issue: "Application failed to start"
**Cause**: Missing environment variables or database connection issue

**Solution**:
1. Go to Render dashboard → Environment
2. Verify ALL 11 environment variables are set:
   - SECRET_KEY
   - DATABASE_URL
   - ADMIN_EMAIL
   - ADMIN_PASSWORD
   - ADMIN_NAME
   - MAIL_SERVER
   - MAIL_PORT
   - MAIL_USE_TLS
   - MAIL_USERNAME
   - MAIL_PASSWORD
   - MAIL_DEFAULT_SENDER
3. Check for typos or extra spaces
4. Click "Manual Deploy" → "Deploy latest commit"

---

### Issue: "502 Bad Gateway"
**Cause**: Application crashed or still starting

**Solution**:
1. Wait 2-3 minutes (app might still be starting)
2. Check Render logs for errors
3. Look for "Application startup complete" message
4. If not found, check database connection

---

### Issue: "Module not found"
**Cause**: Missing dependency in requirements.txt

**Solution**:
1. Add missing module to `requirements.txt`
2. Commit and push to GitHub:
   ```powershell
   git add requirements.txt
   git commit -m "Add missing dependency"
   git push
   ```
3. Render will auto-deploy

---

## 💾 Database Issues

### Issue: "Table does not exist"
**Cause**: Database tables not created

**Solution**:
1. Go to Render dashboard
2. Click "Shell" tab
3. Run database creation commands:
   ```python
   python
   from app import create_app, db
   app = create_app()
   with app.app_context():
       db.create_all()
       print("Database tables created!")
   exit()
   ```

---

### Issue: "Admin user not found"
**Cause**: Admin user not created in database

**Solution**:
1. In Render Shell, run:
   ```python
   python
   from app import create_app, db
   from app.models import User
   from werkzeug.security import generate_password_hash
   
   app = create_app()
   with app.app_context():
       # Check if admin exists
       admin = User.query.filter_by(email='maryygeorge193@gmail.com').first()
       if admin:
           print("Admin already exists!")
       else:
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

## 📧 Email Issues

### Issue: "Email not sending"
**Cause**: Incorrect Gmail credentials or app password

**Solution**:
1. Verify Gmail app password is correct: `bbugpxegjppzyjja`
2. Check environment variables in Render:
   - MAIL_USERNAME = maryygeorge193@gmail.com
   - MAIL_PASSWORD = bbugpxegjppzyjja
3. Make sure 2-factor authentication is enabled on Gmail
4. Verify app password hasn't expired

---

### Issue: "SMTPAuthenticationError"
**Cause**: Wrong password or 2FA not enabled

**Solution**:
1. Go to: https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Generate new App Password:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other"
   - Name it "AIDP"
   - Copy the 16-character password
4. Update MAIL_PASSWORD in Render environment variables

---

## 🌐 Domain Issues

### Issue: "Domain not working"
**Cause**: DNS not propagated yet

**Solution**:
1. Wait 30-60 minutes (DNS propagation takes time)
2. Check DNS propagation: https://dnschecker.org
3. Enter your domain name
4. Should show Render's IP address globally

---

### Issue: "SSL certificate error"
**Cause**: Render hasn't issued SSL yet

**Solution**:
1. Wait 5-10 minutes after adding domain
2. Render automatically provisions SSL certificates
3. Check Render dashboard → Settings → Custom Domains
4. Should show "SSL certificate active"

---

### Issue: "DNS_PROBE_FINISHED_NXDOMAIN"
**Cause**: DNS records not set correctly

**Solution**:
1. Go to your domain registrar
2. Verify DNS records:
   - Type: A, Name: @, Value: [Render IP from dashboard]
   - Type: CNAME, Name: www, Value: your-app.onrender.com
3. Remove any conflicting records
4. Save and wait 30 minutes

---

## 🔐 Login Issues

### Issue: "Invalid credentials" for admin
**Cause**: Admin user not created or wrong password

**Solution**:
1. Verify credentials:
   - Email: maryygeorge193@gmail.com
   - Password: Horlyboi1607
2. If still failing, recreate admin user (see Database Issues above)

---

### Issue: "Session expired" immediately after login
**Cause**: SECRET_KEY not set or changing

**Solution**:
1. Generate a strong SECRET_KEY: https://randomkeygen.com/
2. Set it in Render environment variables
3. DO NOT change it after setting (will invalidate all sessions)

---

## 💬 Chat Issues

### Issue: "Chat not working"
**Cause**: SocketIO connection failed

**Solution**:
1. Check browser console for errors (F12)
2. Verify SocketIO is installed: check `requirements.txt`
3. Clear browser cache: Ctrl + Shift + Delete
4. Try different browser

---

### Issue: "Messages not sending"
**Cause**: Database connection or SocketIO issue

**Solution**:
1. Check Render logs for errors
2. Verify database connection is working
3. Test with simple message
4. Check if messages appear in database (Supabase dashboard)

---

## 📱 Mobile Issues

### Issue: "Layout broken on mobile"
**Cause**: Cache not cleared

**Solution**:
1. On mobile browser, clear cache
2. Hard refresh: 
   - iOS Safari: Hold refresh button → "Request Desktop Site" → reload
   - Android Chrome: Settings → Privacy → Clear browsing data
3. Close and reopen browser

---

## 🔄 Update Issues

### Issue: "Changes not showing after push"
**Cause**: Render not auto-deploying

**Solution**:
1. Go to Render dashboard
2. Click "Manual Deploy"
3. Select "Deploy latest commit"
4. Wait for build to complete
5. Hard refresh browser: Ctrl + Shift + R

---

## 🆘 Emergency Recovery

### Issue: "Everything is broken"
**Solution**: Start fresh with database

1. In Render Shell:
   ```python
   python
   from app import create_app, db
   app = create_app()
   with app.app_context():
       db.drop_all()  # WARNING: Deletes all data!
       db.create_all()
       print("Database reset!")
   exit()
   ```

2. Recreate admin user (see Database Issues above)

3. Test application

---

## 📞 Getting Help

### Check Logs First
1. **Render Logs**: Dashboard → Logs tab
2. **Browser Console**: F12 → Console tab
3. **Supabase Logs**: Dashboard → Logs section

### Useful Commands for Debugging

**Check if app is running**:
```python
python
from app import create_app
app = create_app()
print("App created successfully!")
exit()
```

**Check database connection**:
```python
python
from app import create_app, db
app = create_app()
with app.app_context():
    print(db.engine.url)
exit()
```

**List all users**:
```python
python
from app import create_app, db
from app.models import User
app = create_app()
with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"{user.email} - {user.role}")
exit()
```

---

## 🎯 Prevention Tips

1. **Always test locally first**: Run `python run.py` before deploying
2. **Check logs regularly**: Monitor Render logs for warnings
3. **Backup database**: Export from Supabase dashboard weekly
4. **Document changes**: Keep notes of what you modify
5. **Test after updates**: Always test after pushing changes

---

## 📚 Additional Resources

- **Render Docs**: https://render.com/docs
- **Supabase Docs**: https://supabase.com/docs
- **Flask Docs**: https://flask.palletsprojects.com/
- **Git Docs**: https://git-scm.com/doc

---

## ✅ Quick Health Check

Run this checklist if something seems wrong:

- [ ] Render service is "Live" (green)
- [ ] Supabase project is "Active" (green)
- [ ] All 11 environment variables are set
- [ ] DATABASE_URL is correct
- [ ] Admin user exists in database
- [ ] No errors in Render logs
- [ ] Browser cache is cleared
- [ ] Using latest code from GitHub

---

**Still stuck? Check the specific error message in logs and search for it in this guide.**
