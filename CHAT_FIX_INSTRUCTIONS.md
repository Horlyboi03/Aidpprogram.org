# Chat System Not Working - Troubleshooting Guide

## Issue
Messages showing clock icon (sending) but not delivering (checkmark).

## Root Cause
Socket.IO connection not established properly.

## Steps to Fix

### 1. Check Browser Console (F12)
Open browser console and look for errors like:
- `Socket.IO connection failed`
- `WebSocket connection error`
- `CORS error`

### 2. Verify Server is Running
Make sure Flask server is running with SocketIO:
```bash
python run.py
```

You should see:
```
* Running on http://127.0.0.1:5001
```

### 3. Check Database Migration
The `is_delivered` column must exist:
```bash
python add_is_delivered_column.py
```

### 4. Test Socket Connection
Open browser console on chat page and check for:
```
[AIDP Chat] Initializing chat...
[AIDP Chat] Connected: <socket_id>
```

If you see connection errors, the issue is with Socket.IO setup.

### 5. Common Issues

**Issue: "Socket not connected"**
- Solution: Restart the Flask server

**Issue: "CORS error"**
- Already fixed in code with `cors_allowed_origins='*'`

**Issue: Messages save to database but don't appear**
- Check if both users are on the chat page
- Refresh the page

**Issue: Clock icon stays forever**
- Socket.IO not emitting events properly
- Check server terminal for errors

### 6. Quick Test
1. Open two browser windows
2. Login as admin in one, applicant in other
3. Send message from admin
4. Check if it appears in applicant's chat immediately

If it doesn't appear immediately, Socket.IO is not working.

### 7. Fallback Solution
If Socket.IO continues to fail, we can implement a polling-based chat system that refreshes messages every few seconds instead of real-time.

## Debug Commands

Check if messages are being saved:
```bash
python -c "from app import create_app, db; from app.models import Message; app = create_app(); ctx = app.app_context(); ctx.push(); print('Messages:', Message.query.count())"
```

Check Socket.IO is installed:
```bash
pip show flask-socketio python-socketio
```

## Next Steps
1. Check browser console for errors
2. Share any error messages you see
3. Verify server is running without errors
