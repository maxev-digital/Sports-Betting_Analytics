#!/bin/bash
# Automated Deployment Script for MAX-EV-SPORTS
# Deploys backend and frontend to VPS in one command
# Usage: ./deploy.sh "Your commit message"

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# VPS Configuration
VPS_IP="148.230.87.135"
VPS_USER="root"
SSH_KEY="$HOME/.ssh/hostinger_vps"

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}  MAX-EV-SPORTS Deployment Script${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# Get commit message from argument or use default
COMMIT_MSG="${1:-Update backend and frontend}"

# Step 1: Git Commit and Push
echo -e "${YELLOW}[1/6]${NC} Committing changes to Git..."
if git diff --quiet && git diff --cached --quiet; then
    echo "  ℹ️  No changes to commit"
else
    git add backend/main.py backend/game_tracker.py backend/stripe_service.py backend/espn_nba_client.py backend/config.py
    git add frontend/src/ frontend/public/ frontend/index.html frontend/package.json
    git commit -m "$COMMIT_MSG

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>" || echo "  ℹ️  Nothing to commit"

    echo -e "  ${GREEN}✓${NC} Pushing to GitHub..."
    git push origin main
fi
echo -e "${GREEN}✓ Git commit complete${NC}\n"

# Step 2: Clean and Rebuild Frontend
echo -e "${YELLOW}[2/6]${NC} Rebuilding frontend..."
cd frontend

# Remove old build
rm -rf dist/

# Build fresh
npm run build

echo -e "${GREEN}✓ Frontend build complete${NC}\n"
cd ..

# Step 3: Deploy Backend Files
echo -e "${YELLOW}[3/6]${NC} Deploying backend to VPS..."
scp -i "$SSH_KEY" \
    backend/main.py \
    backend/game_tracker.py \
    backend/stripe_service.py \
    backend/espn_nba_client.py \
    backend/config.py \
    backend/alert_monitor.py \
    backend/auth.py \
    $VPS_USER@$VPS_IP:/root/sporttrader/backend/

echo -e "${GREEN}✓ Backend deployed${NC}\n"

# Step 4: Deploy Frontend Build
echo -e "${YELLOW}[4/6]${NC} Deploying frontend to VPS..."

# Clear old frontend files
ssh -i "$SSH_KEY" $VPS_USER@$VPS_IP "rm -rf /var/www/sporttrader/*"

# Copy new build
scp -i "$SSH_KEY" -r frontend/dist/* $VPS_USER@$VPS_IP:/var/www/sporttrader/

echo -e "${GREEN}✓ Frontend deployed${NC}\n"

# Step 5: Restart Backend Service
echo -e "${YELLOW}[5/6]${NC} Restarting backend service..."
ssh -i "$SSH_KEY" $VPS_USER@$VPS_IP "systemctl restart sporttrader"

# Wait for service to start
sleep 3

echo -e "${GREEN}✓ Service restarted${NC}\n"

# Step 6: Verify Deployment
echo -e "${YELLOW}[6/6]${NC} Verifying deployment..."

# Check backend service
SERVICE_STATUS=$(ssh -i "$SSH_KEY" $VPS_USER@$VPS_IP "systemctl is-active sporttrader")
if [ "$SERVICE_STATUS" = "active" ]; then
    echo -e "  ${GREEN}✓${NC} Backend service: Running"
else
    echo -e "  ${RED}✗${NC} Backend service: Failed"
    ssh -i "$SSH_KEY" $VPS_USER@$VPS_IP "journalctl -u sporttrader -n 20 --no-pager"
    exit 1
fi

# Check frontend files
FRONTEND_CHECK=$(ssh -i "$SSH_KEY" $VPS_USER@$VPS_IP "[ -f /var/www/sporttrader/index.html ] && echo 'ok' || echo 'missing'")
if [ "$FRONTEND_CHECK" = "ok" ]; then
    echo -e "  ${GREEN}✓${NC} Frontend files: Deployed"
else
    echo -e "  ${RED}✗${NC} Frontend files: Missing"
    exit 1
fi

# Check for Casino Tears (should NOT exist)
CASINO_CHECK=$(ssh -i "$SSH_KEY" $VPS_USER@$VPS_IP "ls /var/www/sporttrader/casino* 2>/dev/null || echo 'clean'")
if [ "$CASINO_CHECK" = "clean" ]; then
    echo -e "  ${GREEN}✓${NC} No old branding files"
else
    echo -e "  ${YELLOW}⚠${NC}  Warning: Old files detected: $CASINO_CHECK"
fi

# Check image sliders
SLIDER_CHECK=$(ssh -i "$SSH_KEY" $VPS_USER@$VPS_IP "[ -d /var/www/sporttrader/SliderImages ] && echo 'ok' || echo 'missing'")
if [ "$SLIDER_CHECK" = "ok" ]; then
    echo -e "  ${GREEN}✓${NC} Image sliders: Deployed"
else
    echo -e "  ${YELLOW}⚠${NC}  Warning: SliderImages folder missing"
fi

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  🎉 Deployment Complete!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo -e "Live site: ${BLUE}https://max-ev-sports.com${NC}"
echo -e "API health: ${BLUE}https://max-ev-sports.com/api/games${NC}"
echo ""
echo -e "View logs: ${YELLOW}ssh -i ~/.ssh/hostinger_vps root@$VPS_IP 'journalctl -u sporttrader -f'${NC}"
echo ""
