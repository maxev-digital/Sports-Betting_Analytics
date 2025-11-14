# Max EV Sports - User Credentials

**Website:** https://max-ev-sports.com

---

## 🔐 Primary Admin Account (USE THIS)

| Username | Password | Role | Email |
|----------|----------|------|-------|
| **MaxEVAdmin** | `MaxEV2025!Admin` | Admin | admin@max-ev-sports.com |

**Use this account for:**
- Monitoring user feedback at `/admin-dashboard`
- Viewing all user activity
- Managing the platform
- Daily administrative tasks

## 🔐 Additional Admin Accounts

| Username | Password | Role | Email |
|----------|----------|------|-------|
| **ANP428** | (same as other accounts) | Admin | anp428@max-ev-sports.com |

## 👥 Test User Accounts

| Username | Password | Role | Email |
|----------|----------|------|-------|
| **Terry** | `Simspeed1` | User | user1@max-ev-sports.com |
| **TenTon#1** | `AlexaVesta69` | User | user2@max-ev-sports.com |
| **Sheets** | `Parlinski1` | User | user3@max-ev-sports.com |
| **RickT** | `Rick1` | User | rickt@max-ev-sports.com |

---

## 📊 Admin Features

Admin accounts (`MaxEVAdmin` and `ANP428`) can access:
- **View all users** - See all registered accounts
- **Monitor active sessions** - Who's currently online
- **View activity logs** - Login/logout history
- **User statistics** - Session duration, login counts
- **Feedback monitoring** - View all user feedback submissions

### Admin Endpoints:
```
GET /api/admin/users?token=ADMIN_TOKEN
GET /api/admin/active-sessions?token=ADMIN_TOKEN
GET /api/admin/activity-log?token=ADMIN_TOKEN
GET /api/admin/all-user-stats?token=ADMIN_TOKEN
GET /api/feedback/all - View all feedback (requires admin login)
```

### Feedback Dashboard:
- **URL:** https://max-ev-sports.com/admin-dashboard
- **Purpose:** Monitor bugs, feature requests, and general feedback from users
- **Data Location:** `/root/sporttrader/backend/data/feedback/user_feedback.json`

---

## 🔒 Security Features

- **Session Duration:** 7 days (auto-logout after inactivity)
- **Password Storage:** SHA256 hashed
- **Activity Tracking:** All logins/logouts logged with timestamps
- **Session Monitoring:** Track duration and activity count

---

## 📝 Notes

- All accounts are active and ready to use
- Users can change their passwords after logging in
- Admin can monitor all user activity
- Sessions persist for 7 days unless manually logged out

---

**Updated:** November 4, 2025
**Site:** https://max-ev-sports.com
**Branding:** Max EV Sports - Maximum EV Is Our Specialty
