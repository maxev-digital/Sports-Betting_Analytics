# Discord Server Setup - Quick Reference

## What Was Done

✅ Added Discord invite link to welcome email: `https://discord.gg/BhXfb4eE`
✅ Created comprehensive Discord server automation scripts
✅ Ready to automatically create 60+ channels, 12 categories, and 7 roles

## Files Created

All files are located in: `backend/ARB_Auto_Bettor/`

1. **DISCORD_BOT_SETUP_GUIDE.md** - Complete step-by-step guide
2. **discord_server_setup.py** - Automation script (creates everything)
3. **.env.template** - Template for bot credentials

## Discord Server Structure

The script will create:

### Categories & Channels (12 categories, 60+ channels)
- 📋 **WELCOME & INFO** - Welcome, rules, announcements, start-here, links
- 🚨 **LIVE ALERTS** - Arb, middles, steam, goalie pulls, live steam, EV plays
- 🏀 **NBA** - General, predictions, lines, picks
- 🏈 **NFL** - General, predictions, lines, picks
- 🏒 **NHL** - General, predictions, goalie pulls, picks
- ⚾ **MLB** - General, predictions, picks
- 🏀 **COLLEGE BASKETBALL** - General, predictions, picks
- ⚽ **OTHER SPORTS** - Soccer, MMA/Boxing, Tennis, other
- 📊 **ANALYTICS & TOOLS** - Analytics, bot commands, extension help, platform help, backtesting
- 🎓 **EDUCATION** - Strategies, glossary, FAQs, tutorials, bankroll management
- 💬 **COMMUNITY** - General, wins, bad beats, memes, screenshots, off-topic
- 🛠️ **SUPPORT** - Support, feedback, bug reports, changelog

### Roles (7 roles with permissions)
- 👑 Admin (full permissions)
- 🛡️ Moderator (kick, ban, manage messages)
- 💎 Premium (displayed separately)
- 📊 Analytics Pro (displayed separately)
- 🎯 Active Bettor (displayed separately)
- 📱 Extension User
- 🆕 New Member

## Quick Start (When Ready)

### Step 1: Create Discord Bot (5 minutes)
```
1. Go to: https://discord.com/developers/applications
2. Create new application: "MAX-EV Sports Setup Bot"
3. Go to Bot → Add Bot → Copy Token
4. Enable: SERVER MEMBERS INTENT + MESSAGE CONTENT INTENT
5. OAuth2 → URL Generator → Select "bot" + "Administrator"
6. Use generated URL to invite bot to your server
```

### Step 2: Install Requirements
```bash
pip install discord.py python-dotenv
```

### Step 3: Configure
```bash
cd backend/ARB_Auto_Bettor
# Copy .env.template to .env and add:
# DISCORD_BOT_TOKEN=your_token_here
# DISCORD_GUILD_ID=your_server_id_here
```

### Step 4: Run Setup
```bash
python discord_server_setup.py
```

Script takes 1-2 minutes and creates everything automatically!

## Discord Invite Link

Server invite: **https://discord.gg/BhXfb4eE**

This link is now included in the welcome email template at:
`backend/ARB_Auto_Bettor/WELCOME_EMAIL_TEMPLATE.md`

## Documentation

Full guide with screenshots and troubleshooting:
`backend/ARB_Auto_Bettor/DISCORD_BOT_SETUP_GUIDE.md`

## Notes

- Script is safe to re-run (skips existing channels)
- Automatically handles Discord rate limits
- Creates welcome embed message in #welcome
- All channels have descriptions pre-configured
- Roles have color coding and permissions set

## Next Steps (After Setup)

1. Customize welcome message
2. Add channel icons/banners
3. Set up auto-moderator
4. Configure role permissions
5. Add webhooks for live alerts (optional)
6. Pin important messages in key channels

---

**Status:** Ready to use when needed. All files prepared.
**Location:** `C:\Users\nashr\backend\ARB_Auto_Bettor\`
