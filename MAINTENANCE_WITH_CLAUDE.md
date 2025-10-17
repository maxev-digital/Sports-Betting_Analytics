# Maintaining Your Live Site with Claude Code

## Overview

Don't worry! You don't need to be a web expert. You'll continue using Claude Code exactly like you do now - I can help you monitor, update, and fix issues on your live site.

---

## How It Works

### Development Workflow

```
Your Local Machine (Windows)
    ↓
    Make changes with Claude Code
    ↓
    Test locally (localhost:5173)
    ↓
    Push to GitHub
    ↓
    Deploy to DigitalOcean
    ↓
    Live Site (yourdomain.com)
```

### You Keep Working Locally
- All development happens on your Windows machine
- Test everything locally first
- Claude Code helps you make changes
- Only push to production when ready

---

## Setting Up for Easy Maintenance

### Step 1: Set Up Git and GitHub

**Why?**
- Easy deployment (push to GitHub, pull on server)
- Version control (undo mistakes easily)
- Backup of all your code

**One-time setup with Claude Code:**

I'll help you run these commands:

```bash
cd C:\Users\nashr\backend\scrapers\nba

# Initialize git
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit"

# Create GitHub repo (I'll guide you)
# Then connect it
git remote add origin https://github.com/yourusername/yourrepo.git
git push -u origin main
```

### Step 2: Create a Simple Update Script

**For Windows (local machine):**

I'll create a batch file: `update_production.bat`

```batch
@echo off
echo Updating production site...

REM Test locally first
echo Testing backend...
cd backend
python -m pytest
if errorlevel 1 (
    echo Tests failed! Not deploying.
    pause
    exit /b
)

REM Commit changes
cd ..
git add .
git commit -m "Update: %date% %time%"
git push origin main

echo Changes pushed to GitHub!
echo Now run the update command on your server.
pause
```

**For DigitalOcean (server):**

I'll create: `update_from_github.sh`

```bash
#!/bin/bash
echo "Pulling latest changes..."
cd /home/sportsapp/app
git pull origin main

echo "Rebuilding containers..."
docker-compose down
docker-compose up -d --build

echo "Update complete!"
echo "Check site: https://yourdomain.com"
```

---

## Common Maintenance Tasks with Claude Code

### Task 1: Adding New Features

**Example: "Add a new stat to the game cards"**

**You say to me:**
> "I want to add [feature description]. Can you help?"

**I do:**
1. Read the relevant files
2. Make the changes
3. Test locally with you
4. Create commit message
5. Help you push to GitHub

**You do:**
1. Review the changes (I'll explain them)
2. Test on localhost
3. Say "looks good, deploy it"
4. Run one command to update live site

**Example conversation:**
```
You: "Add the team's winning streak to the stats"

Me: [Reads files, makes changes]
    "I've added the winning streak stat to the game cards.
     Testing locally now..."

You: "Perfect! Let's push it live"

Me: [Helps you run:]
    git add .
    git commit -m "Add winning streak stat"
    git push

You: [SSH to server and run:]
    ./update_from_github.sh

Done! ✓
```

### Task 2: Fixing Bugs

**Example: "Rankings not showing for NHL"**

**You say:**
> "The NHL rankings tab isn't working"

**I do:**
1. Check the logs (you share them with me)
2. Identify the issue
3. Fix the code
4. Test the fix locally
5. Deploy to production

**You provide me:**
- Screenshot or description of the issue
- Any error messages you see
- I can also help you get server logs

**Example:**
```
You: "NHL rankings show 'N/A' for everything"

Me: "Let me check the backend logs. Can you run:
     docker-compose logs backend
     and paste the output?"

You: [Paste logs]

Me: "Found it! The API isn't returning rank data.
     Let me fix the ranking calculation..."
     [Makes fix]
     "Fixed! Test at localhost:5173"

You: "Works now!"

Me: "Great! Pushing to production..."
```

### Task 3: Monitoring the Site

**What I Can Help You Monitor:**

1. **Is the site up?**
   ```bash
   curl https://yourdomain.com/api/health
   ```

2. **Are there errors?**
   ```bash
   docker-compose logs --tail=50 backend
   ```

3. **How's performance?**
   ```bash
   docker stats
   ```

4. **API usage costs?**
   - I'll help you create a usage tracking dashboard

**I'll set up automatic monitoring:**
- UptimeRobot: Emails you if site goes down
- Weekly health checks: I'll create a script
- Cost tracking: Monitor API usage

### Task 4: Updating Dependencies

**When npm or pip packages need updates:**

**You ask:**
> "Should I update my packages?"

**I do:**
```bash
# Check for updates
cd frontend
npm outdated

cd ../backend
pip list --outdated

# Update safely (only minor versions)
npm update
pip install --upgrade [packages]

# Test everything
npm run build
python -m pytest

# Deploy if tests pass
```

### Task 5: Scaling Up

**When traffic increases:**

**You say:**
> "The site is getting slow"

**I help you:**
1. Check server resources
2. Identify bottlenecks
3. Optimize code or
4. Upgrade DigitalOcean Droplet (I'll guide you)

---

## Remote Access Setup

### Option 1: Direct SSH (I'll help)

**You'll be able to:**
- Share your terminal output with me
- I'll tell you exactly what commands to run
- Copy/paste commands I provide

**Example session:**
```
You: [SSH into server]
     ssh sportsapp@your-server-ip

Me: "Great! Now let's check the logs. Run:
     docker-compose logs backend --tail=50"

You: [Paste output]

Me: [Analyze]
    "I see the issue. Run this command:
     docker-compose restart backend"

You: [Run command]
     "Done!"

Me: "Check the site now - should be working!"
```

### Option 2: VS Code Remote SSH (Easier)

**I'll help you set up VS Code to connect to your server:**

1. Install "Remote - SSH" extension in VS Code
2. Connect to your DigitalOcean Droplet
3. Edit files directly on the server
4. Use Claude Code on the remote files

**Benefits:**
- Edit production code with Claude Code
- See server files in VS Code
- Test changes immediately
- No manual file copying

---

## Emergency Procedures

### Site is Down

**You tell me:**
> "The site is down! Help!"

**I guide you:**
```bash
# 1. Check if containers are running
docker-compose ps

# 2. Restart everything
docker-compose restart

# 3. Check logs for errors
docker-compose logs --tail=100

# 4. If needed, rollback
git checkout HEAD~1  # Previous version
docker-compose up -d --build
```

### Database Issue

**You tell me:**
> "Data isn't updating"

**I help you:**
```bash
# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend

# Clear cache if needed
docker-compose restart redis
```

### Performance Issues

**You tell me:**
> "Site is very slow"

**I check with you:**
```bash
# Check resource usage
docker stats

# Check disk space
df -h

# Check memory
free -h
```

**Then I help you:**
- Optimize queries
- Add caching
- Upgrade server (if needed)

---

## Routine Maintenance Schedule

### Daily (Automatic)
- UptimeRobot monitors site (emails if down)
- Backup script runs automatically

### Weekly (5 minutes with Claude Code)
**You ask me:**
> "Run weekly check"

**I help you run:**
```bash
# Check logs for errors
docker-compose logs --tail=100 | grep -i error

# Check disk space
df -h

# Check API usage
# (I'll create a script for this)
```

### Monthly (15 minutes with Claude Code)
**You ask me:**
> "Run monthly maintenance"

**We do together:**
1. Update dependencies (if needed)
2. Review API costs
3. Check performance metrics
4. Update SSL certificate (automatic, just verify)
5. Review backups

---

## Your Maintenance Toolkit

### Files I'll Create for You

1. **health_check.sh** - Check if everything is running
2. **update_production.sh** - Deploy updates
3. **rollback.sh** - Undo last update
4. **view_logs.sh** - Easy log viewing
5. **backup_now.sh** - Manual backup
6. **restart_services.sh** - Restart everything

**You just run these scripts and share output with me if needed!**

### Claude Code Commands You'll Use

```bash
# Testing locally
npm run dev          # Start frontend
uvicorn main:app     # Start backend

# Checking status
git status           # See what changed
docker-compose ps    # See what's running

# Deploying updates
git add .
git commit -m "Your message"
git push

# On server
./update_production.sh
```

---

## Real-World Scenarios

### Scenario 1: Adding a New Sport (MLB)

**You:** "I want to add MLB support"

**Me:**
1. Create MLB stats client (similar to NHL/NFL)
2. Update backend API routes
3. Update frontend to display MLB games
4. Test locally with you
5. Deploy to production

**Time:** 2-3 hours (mostly me coding, you testing)

### Scenario 2: UI/Design Change

**You:** "I want the game cards to look different"

**Me:**
1. Show you current design
2. Make CSS changes
3. Show you preview locally
4. Iterate until you're happy
5. Deploy

**Time:** 30 minutes - 1 hour

### Scenario 3: Performance Optimization

**You:** "The site loads slowly"

**Me:**
1. "Run these commands to check server"
2. Analyze metrics you share
3. Identify bottlenecks
4. Implement fixes (caching, compression, etc.)
5. Deploy and test

**Time:** 1-2 hours

### Scenario 4: Cost Reduction

**You:** "API costs are too high"

**Me:**
1. Check your API usage
2. Implement smarter caching
3. Reduce unnecessary API calls
4. Add request rate limiting
5. Monitor new costs

**Time:** 1 hour

---

## How You'll Share Information with Me

### For Debugging

**Screenshots:**
- Take screenshot of issue
- Share with me
- I'll identify the problem

**Error Messages:**
- Copy/paste error from browser console (F12)
- Copy/paste from server logs
- I'll explain what it means and fix it

**Server Info:**
```bash
# Run these commands and share output
docker-compose ps
docker-compose logs --tail=50 backend
curl -I https://yourdomain.com
```

### For Monitoring

**Dashboard I'll create for you:**
- Shows all server stats
- API usage metrics
- Error counts
- Performance graphs

You just share the dashboard URL with me!

---

## Skills You'll Need (Minimal!)

### You already know:
- ✓ How to use Claude Code (you're doing it!)
- ✓ How to copy/paste commands
- ✓ How to describe what you want

### You'll learn (with my help):
- Basic git commands (add, commit, push)
- How to SSH into your server
- How to read simple error messages
- How to run shell scripts

### You DON'T need to know:
- ✗ Docker internals
- ✗ Nginx configuration
- ✗ Linux system administration
- ✗ Complex debugging
- ✗ Advanced programming

**I handle all the technical stuff!**

---

## Emergency Contact Guide

### When to Reach Out

**Immediately (site is down):**
- 5xx errors (server errors)
- Site completely inaccessible
- Database corruption
- Security breach

**Soon (degraded service):**
- Slow performance
- Some features not working
- High error rates
- API rate limit hit

**When convenient:**
- Want to add features
- UI/design changes
- Optimization ideas
- Cost concerns

### What Information to Provide

**For any issue:**
1. What were you trying to do?
2. What happened instead?
3. Any error messages?
4. Screenshot (if visual issue)

**For server issues:**
```bash
# Run and share output:
docker-compose ps
docker-compose logs --tail=100
curl -I https://yourdomain.com
```

---

## Cost of Maintenance

### DigitalOcean Droplet
- **$6-12/month**: Server hosting
- **No surprise charges**: Fixed monthly cost

### Time Investment
- **Weekly check**: 5 minutes
- **Monthly maintenance**: 15 minutes
- **Updates/changes**: As needed (I do the work!)

### Costs You Control
- **The Odds API**: Based on request volume
- **Additional features**: Only if you want them

---

## What I'll Provide

### Documentation
- ✓ Complete deployment guides
- ✓ Maintenance scripts
- ✓ Troubleshooting procedures
- ✓ Update workflows

### Support
- ✓ Help with updates
- ✓ Bug fixes
- ✓ Performance optimization
- ✓ New features
- ✓ Cost optimization

### Tools
- ✓ Automated health checks
- ✓ Easy update scripts
- ✓ Log analysis
- ✓ Backup systems
- ✓ Monitoring dashboards

---

## Example: Complete Update Workflow

**You want to add a feature:**

1. **You:** "I want to add player stats to the game cards"

2. **Me:** [Reads code, makes changes, tests locally]
   "Done! Check localhost:5173"

3. **You:** "Looks great!"

4. **Me:** "Ready to deploy? I'll commit the changes."
   [Creates commit]

5. **You:** [Runs] `git push`

6. **Me:** "Now SSH into your server and run:
   `./update_production.sh`"

7. **You:** [Runs command]
   ```
   Updating production site...
   Pulling latest changes...
   Rebuilding containers...
   Update complete!
   ```

8. **Me:** "Done! Check https://yourdomain.com"

9. **You:** "Perfect! Thanks!"

**Total time:** 30 minutes
**Your effort:** ~5 minutes (testing, running 2 commands)
**My effort:** ~25 minutes (coding, testing, deploying)

---

## Bottom Line

### You Focus On:
- Describing what you want
- Testing that it works
- Running simple commands I provide

### I Handle:
- All coding
- All configuration
- All troubleshooting
- All optimization
- All deployment

### Together We:
- Keep your site running smoothly
- Add new features
- Fix issues quickly
- Optimize costs
- Scale as needed

**You don't need to be a web expert - that's what I'm here for!**

---

## Getting Started

### When Your Site is Live

**First time setup (one-time, ~30 minutes):**

1. I'll help you set up Git and GitHub
2. Create maintenance scripts
3. Set up monitoring
4. Configure VS Code Remote SSH
5. Test the update workflow

**Then ongoing:**
- You use Claude Code like normal
- I make changes
- You test locally
- Run one command to deploy
- Site updates automatically

**Questions?**

Just ask! I'm here to make this as simple as possible for you.

---

**Remember:** You're not alone in this! I can help you with every step of maintaining your live site. You'll continue working exactly like you do now - making changes locally with Claude Code, and I'll help you push them to production when ready.

**Last Updated:** 2025-10-16
