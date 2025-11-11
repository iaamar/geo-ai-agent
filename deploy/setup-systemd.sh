#!/bin/bash

# GEO Expert Agent - systemd Service Setup Script
# This script sets up systemd services to keep the app running

set -e

echo "═══════════════════════════════════════════════════════════"
echo "   GEO Expert Agent - systemd Service Setup"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run with sudo:"
    echo "   sudo bash deploy/setup-systemd.sh"
    exit 1
fi

# Get the current user (who invoked sudo)
REAL_USER=${SUDO_USER:-$USER}
REAL_HOME=$(eval echo ~$REAL_USER)
PROJECT_DIR=$(pwd)

echo "📁 Project directory: $PROJECT_DIR"
echo "👤 Running as user: $REAL_USER"
echo ""

# Check if service files exist
if [ ! -f "deploy/geo-agent.service" ] || [ ! -f "deploy/geo-agent-frontend.service" ]; then
    echo "❌ Service files not found!"
    echo "   Make sure you're in the project root directory"
    exit 1
fi

# Update service files with actual paths
echo "📝 Updating service files with correct paths..."

# Update backend service
sed -i "s|WorkingDirectory=.*|WorkingDirectory=$PROJECT_DIR|g" deploy/geo-agent.service
sed -i "s|ExecStart=.*|ExecStart=$PROJECT_DIR/.venv/bin/python -m src.main|g" deploy/geo-agent.service
sed -i "s|EnvironmentFile=.*|EnvironmentFile=$PROJECT_DIR/.env|g" deploy/geo-agent.service
sed -i "s|User=.*|User=$REAL_USER|g" deploy/geo-agent.service

# Update frontend service
sed -i "s|WorkingDirectory=.*|WorkingDirectory=$PROJECT_DIR/frontend|g" deploy/geo-agent-frontend.service
sed -i "s|User=.*|User=$REAL_USER|g" deploy/geo-agent-frontend.service

# Copy service files
echo "📋 Copying service files to /etc/systemd/system/..."
cp deploy/geo-agent.service /etc/systemd/system/
cp deploy/geo-agent-frontend.service /etc/systemd/system/

# Reload systemd
echo "🔄 Reloading systemd daemon..."
systemctl daemon-reload

# Enable services (start on boot)
echo "✅ Enabling services (auto-start on boot)..."
systemctl enable geo-agent.service
systemctl enable geo-agent-frontend.service

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "   Setup Complete!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Start the services:"
echo "   sudo systemctl start geo-agent.service"
echo "   sudo systemctl start geo-agent-frontend.service"
echo ""
echo "2. Check status:"
echo "   sudo systemctl status geo-agent.service"
echo "   sudo systemctl status geo-agent-frontend.service"
echo ""
echo "3. View logs:"
echo "   sudo journalctl -u geo-agent.service -f"
echo "   sudo journalctl -u geo-agent-frontend.service -f"
echo ""
echo "4. Stop services:"
echo "   sudo systemctl stop geo-agent.service"
echo "   sudo systemctl stop geo-agent-frontend.service"
echo ""
echo "5. Restart services:"
echo "   sudo systemctl restart geo-agent.service"
echo "   sudo systemctl restart geo-agent-frontend.service"
echo ""
echo "═══════════════════════════════════════════════════════════"

