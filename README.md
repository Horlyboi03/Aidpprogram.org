# 🌐 AIDP — Agency for International Development Program

A modern, full-stack grant application portal built with Flask, PostgreSQL, and Socket.IO.

---

## ⚡ Quick Start

### 1. Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | 3.10+   |
| PostgreSQL  | 13+     |

### 2. Create the PostgreSQL Database

Open psql and run:

```sql
CREATE DATABASE aidp_db;
```

### 3. Configure Environment

Edit `.env` with your real database credentials:

```ini
SECRET_KEY=your-very-secret-key
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/aidp_db
ADMIN_EMAIL=admin@aidp.org
ADMIN_PASSWORD=Admin@1234
ADMIN_NAME=AIDP Administrator
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 5. Run the Application

```powershell
python run.py
```

The app will be available at **http://localhost:5000**

> Tables are created automatically on first run.
> The admin account is seeded automatically on first run.

---

## 🔑 Default Credentials

| Role  | Email             | Password    |
|-------|-------------------|-------------|
| Admin | admin@aidp.org   | Admin@1234  |

Change these in your `.env` before deploying to production!

---

## 📁 Project Structure

```
new ai/
├── app/
│   ├── __init__.py          # App factory, extensions
│   ├── models.py            # SQLAlchemy models
│   ├── sockets.py           # Flask-SocketIO events
│   ├── routes/
│   │   ├── auth.py          # Register / Login / Logout
│   │   ├── user.py          # Home, Dashboard, Apply, Chat
│   │   ├── admin.py         # Admin Dashboard, Users, Applications
│   │   └── chat.py          # Chat history API
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/            # Login, Register
│   │   ├── user/            # Home, Dashboard, Apply, Chat
│   │   ├── admin/           # Dashboard, Applications, Users, Chat
│   │   └── errors/          # 403, 404
│   └── static/
│       ├── css/style.css
│       └── js/chat.js
├── config.py
├── run.py
├── requirements.txt
└── .env
```

---

## 🚀 Features

### Applicant Side
- **Register / Login** — Secure password hashing (Werkzeug)
- **Grant Application** — Full form: personal, financial, and grant details
- **Dashboard** — Track application status (Pending / Approved / Rejected)
- **Live Chat** — Real-time messaging with AIDP admin

### Admin Side
- **Dashboard** — Stats overview (users, pending, approved, rejected)
- **Applications** — View all, filter by status, approve / reject / delete
- **Users** — See all registered applicants with online status
- **Chat** — Select any user and chat in real-time

---

## 🔒 Security

- CSRF protection on all forms (Flask-WTF)
- Password hashing (Werkzeug `generate_password_hash`)
- Role-based access control (admin decorator)
- Session management (Flask-Login)
- XSS-safe chat rendering (HTML escaping in JS)

---

## 💬 Real-Time Chat

Built with **Flask-SocketIO** + **eventlet**:
- Users join a personal socket room on connect
- Messages are persisted to PostgreSQL immediately
- Both sender and recipient receive the message instantly
- Online/offline status tracked per connection

---

## 🗄️ Database Models

| Model       | Key Fields |
|-------------|-----------|
| User        | id, name, email, password_hash, role, is_online |
| Application | user_id FK, full_name, grant_amount ($100K–$450K), status |
| Message     | sender_id FK, recipient_id FK, body, timestamp, is_read |
