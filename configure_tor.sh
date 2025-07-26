#!/bin/bash

# TOR Configuration Script for GHOST PASS
# This script helps configure TOR without requiring sudo access

echo "🔧 TOR Configuration for GHOST PASS"
echo "===================================="

# Check if TOR is installed
if ! command -v tor &> /dev/null; then
    echo "❌ TOR is not installed"
    echo ""
    echo "📦 To install TOR, run:"
    echo "  sudo apt update"
    echo "  sudo apt install -y tor"
    echo ""
    echo "After installation, run this script again."
    exit 1
fi

echo "✅ TOR is installed"

# Check if TOR service is running
if sudo systemctl is-active --quiet tor; then
    echo "✅ TOR service is running"
else
    echo "⚠️  TOR service is not running"
    echo ""
    echo "🚀 To start TOR service:"
    echo "  sudo systemctl start tor"
    echo "  sudo systemctl enable tor"
    echo ""
fi

# Check TOR configuration
echo "🔍 Checking TOR configuration..."

# Create a user-specific TOR configuration
USER_TOR_DIR="$HOME/.ghostpass/tor"
mkdir -p "$USER_TOR_DIR"

# Create user TOR configuration
cat > "$USER_TOR_DIR/torrc" << 'EOF'
# GHOST PASS User TOR Configuration
SocksPort 9050
ControlPort 9051
CookieAuthentication 1
DataDirectory /home/darknight/.ghostpass/tor/data
PidFile /home/darknight/.ghostpass/tor/tor.pid
Log notice stdout
MaxCircuitDirtiness 600
NewCircuitPeriod 30
EnforceDistinctSubnets 1
UseEntryGuards 1
NumEntryGuards 6
GuardLifetime 2592000
CircuitBuildTimeout 30
LearnCircuitBuildTimeout 1
CircuitStreamTimeout 300
MaxClientCircuitsPending 32
MaxOnionQueueDelay 1750
NewOnionKey 1
SafeLogging 1
EOF

echo "✅ User TOR configuration created at $USER_TOR_DIR/torrc"

# Create data directory
mkdir -p "$USER_TOR_DIR/data"

# Create startup script
cat > "$USER_TOR_DIR/start_tor.sh" << 'EOF'
#!/bin/bash
# Start TOR for GHOST PASS

TOR_DIR="$HOME/.ghostpass/tor"
TOR_CONFIG="$TOR_DIR/torrc"
TOR_DATA="$TOR_DIR/data"
TOR_PID="$TOR_DIR/tor.pid"

echo "🚀 Starting TOR for GHOST PASS..."

# Check if TOR is already running
if [ -f "$TOR_PID" ]; then
    PID=$(cat "$TOR_PID")
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ TOR is already running (PID: $PID)"
        exit 0
    else
        echo "⚠️  Removing stale PID file"
        rm -f "$TOR_PID"
    fi
fi

# Start TOR
tor --config "$TOR_CONFIG" --data "$TOR_DATA" --pidfile "$TOR_PID" &

# Wait for TOR to start
echo "⏳ Waiting for TOR to start..."
sleep 5

# Check if TOR started successfully
if [ -f "$TOR_PID" ]; then
    PID=$(cat "$TOR_PID")
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ TOR started successfully (PID: $PID)"
        echo "🔗 SOCKS proxy available at 127.0.0.1:9050"
        echo "🎛️  Control port available at 127.0.0.1:9051"
    else
        echo "❌ TOR failed to start"
        exit 1
    fi
else
    echo "❌ TOR failed to start"
    exit 1
fi
EOF

# Make startup script executable
chmod +x "$USER_TOR_DIR/start_tor.sh"

# Create stop script
cat > "$USER_TOR_DIR/stop_tor.sh" << 'EOF'
#!/bin/bash
# Stop TOR for GHOST PASS

TOR_DIR="$HOME/.ghostpass/tor"
TOR_PID="$TOR_DIR/tor.pid"

echo "🛑 Stopping TOR..."

if [ -f "$TOR_PID" ]; then
    PID=$(cat "$TOR_PID")
    if ps -p $PID > /dev/null 2>&1; then
        kill $PID
        echo "✅ TOR stopped (PID: $PID)"
        rm -f "$TOR_PID"
    else
        echo "⚠️  TOR process not found"
        rm -f "$TOR_PID"
    fi
else
    echo "⚠️  TOR PID file not found"
fi
EOF

# Make stop script executable
chmod +x "$USER_TOR_DIR/stop_tor.sh"

echo ""
echo "✅ TOR configuration completed!"
echo ""
echo "📋 Usage:"
echo "  Start TOR:  $USER_TOR_DIR/start_tor.sh"
echo "  Stop TOR:   $USER_TOR_DIR/stop_tor.sh"
echo ""
echo "🔧 Alternative: Use system TOR service"
echo "  sudo systemctl start tor"
echo "  sudo systemctl stop tor"
echo ""
echo "🧪 Test TOR connection:"
echo "  curl --socks5 127.0.0.1:9050 https://check.torproject.org/"
echo "" 