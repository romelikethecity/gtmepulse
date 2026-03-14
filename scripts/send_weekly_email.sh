#!/bin/bash
# Weekly email send script - run via cron every Monday at 10 AM PST
#
# Server cron entry (add with: crontab -e):
#   0 18 * * 1 /bin/bash /home/rome/gtmepulse/scripts/send_weekly_email.sh >> /home/rome/logs/gtme_email.log 2>&1
#   (18:00 UTC = 10:00 AM PST)
#
# Prerequisites:
#   - .env with RESEND_API_KEY and RESEND_AUDIENCE_ID
#   - Domain verified in Resend (gtmepulse.com)
#   - resend + requests packages in PYTHON path

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$PROJECT_DIR/logs"
DATE=$(date +%Y-%m-%d)

# Use scrapers venv if on server, otherwise system python
if [ -f "/home/rome/scrapers/venv/bin/python3" ]; then
    PYTHON="/home/rome/scrapers/venv/bin/python3"
else
    PYTHON="python3"
fi

mkdir -p "$LOG_DIR"
mkdir -p /home/rome/logs 2>/dev/null || true

echo "=============================="
echo "GTME Pulse Weekly Email — $DATE"
echo "=============================="

# Load env if exists
if [ -f "$PROJECT_DIR/.env" ]; then
    export $(grep -v '^#' "$PROJECT_DIR/.env" | xargs)
fi

cd "$PROJECT_DIR"

# Pull latest code (in case generators were updated)
git pull --rebase --autostash 2>/dev/null || true

# Send the weekly email
echo "[$(date)] Sending weekly email..."
$PYTHON scripts/generate_weekly_email.py --send

echo "[$(date)] Done!"
