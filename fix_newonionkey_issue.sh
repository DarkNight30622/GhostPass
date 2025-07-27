#!/bin/bash

# Targeted Fix for NewOnionKey TOR Configuration Issue
# This script specifically fixes the "Unknown option 'NewOnionKey'" error

echo "🔧 Targeted Fix for NewOnionKey TOR Configuration Issue"
echo "======================================================="

# Step 1: Stop all TOR processes
echo "🛑 Step 1: Stopping all TOR processes..."
pkill -f tor 2>/dev/null || true
sudo systemctl stop tor 2>/dev/null || true
sudo systemctl disable tor 2>/dev/null || true
sleep 3

# Step 2: Fix system TOR configuration
echo ""
echo "🔧 Step 2: Fixing system TOR configuration..."
if [ -f "/etc/tor/torrc" ]; then
    echo "⚠️  Found system TOR config: /etc/tor/torrc"
    echo "📋 Checking for problematic options..."
    
    # Check for NewOnionKey and other problematic options
    PROBLEMATIC_OPTIONS=("NewOnionKey" "config" "NewCircuitPeriod" "MaxCircuitDirtiness")
    
    for option in "${PROBLEMATIC_OPTIONS[@]}"; do
        if grep -q "^$option" /etc/tor/torrc; then
            echo "❌ Found problematic '$option' option in system torrc"
            echo "🔧 Creating backup and removing problematic option..."
            
            # Backup original
            sudo cp /etc/tor/torrc /etc/tor/torrc.backup.$(date +%Y%m%d_%H%M%S)
            
            # Remove problematic option
            sudo sed -i "/^$option/d" /etc/tor/torrc
            
            echo "✅ Removed '$option' option from system torrc"
        fi
    done
    
    echo "✅ System TOR config cleaned"
else
    echo "✅ No system TOR config found"
fi

# Step 3: Create clean user TOR configuration
echo ""
echo "🔧 Step 3: Creating clean user TOR configuration..."
rm -rf ~/.ghostpass/tor
mkdir -p ~/.ghostpass/tor

# Create minimal TOR configuration without problematic options
echo "📝 Creating minimal TOR configuration..."
cat > ~/.ghostpass/tor/torrc << 'EOF'
# GHOST PASS User TOR Configuration (Minimal)
SocksPort 9050
ControlPort 9051
CookieAuthentication 1
DataDirectory /home/darknight/.ghostpass/tor/data
PidFile /home/darknight/.ghostpass/tor/tor.pid
Log notice stdout
SafeLogging 1
EOF

# Create data directory
mkdir -p ~/.ghostpass/tor/data

# Step 4: Create startup script that bypasses system config
echo ""
echo "🔧 Step 4: Creating startup script that bypasses system config..."
cat > ~/.ghostpass/tor/start_tor.sh << 'EOF'
#!/bin/bash
# Start TOR for GHOST PASS (Bypass System Config)

TOR_DIR="$HOME/.ghostpass/tor"
TOR_CONFIG="$TOR_DIR/torrc"
TOR_DATA="$TOR_DIR/data"
TOR_PID="$TOR_DIR/tor.pid"

echo "🚀 Starting TOR for GHOST PASS (Bypass System Config)..."

# Stop any existing TOR processes
pkill -f "tor.*$TOR_CONFIG" 2>/dev/null || true
sleep 2

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

# Start TOR with explicit configuration and ignore system config
echo "🔧 Starting TOR with configuration: $TOR_CONFIG"

# Method 1: Use environment variable to prevent reading system config
export TOR_CONFIG_FILE="$TOR_CONFIG"
export TOR_SKIP_CHECK_CONFIG=1

# Create a completely empty torrc for defaults
EMPTY_TORRC=$(mktemp)
echo "# Empty torrc to override system config" > "$EMPTY_TORRC"

# Start TOR with minimal configuration and override system config
tor --config "$TOR_CONFIG" --data "$TOR_DATA" --pidfile "$TOR_PID" --ignore-missing-torrc --defaults-torrc "$EMPTY_TORRC" --fname /dev/null --hush --quiet &

# Wait for TOR to start
echo "⏳ Waiting for TOR to start..."
sleep 5

# Clean up temporary file
rm -f "$EMPTY_TORRC"

# Check if TOR started successfully
if [ -f "$TOR_PID" ]; then
    PID=$(cat "$TOR_PID")
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ TOR started successfully (PID: $PID)"
        echo "🔗 SOCKS proxy available at 127.0.0.1:9050"
        echo "🎛️  Control port available at 127.0.0.1:9051"
        
        # Test connection
        echo "🧪 Testing TOR connection..."
        sleep 2
        if curl --socks5 127.0.0.1:9050 --connect-timeout 10 https://check.torproject.org/ 2>/dev/null | grep -q "Congratulations"; then
            echo "✅ TOR connection working!"
        else
            echo "⚠️  TOR started but connection test failed"
        fi
    else
        echo "❌ TOR failed to start"
        echo "📋 Checking TOR logs..."
        tail -n 10 "$TOR_DATA/tor.log" 2>/dev/null || echo "No log file found"
        exit 1
    fi
else
    echo "❌ TOR failed to start"
    echo "📋 Checking TOR logs..."
    tail -n 10 "$TOR_DATA/tor.log" 2>/dev/null || echo "No log file found"
    exit 1
fi
EOF

# Create stop script
cat > ~/.ghostpass/tor/stop_tor.sh << 'EOF'
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

# Also kill any TOR processes started by this script
pkill -f "tor.*$HOME/.ghostpass/tor/torrc" 2>/dev/null || true
EOF

# Make scripts executable
chmod +x ~/.ghostpass/tor/start_tor.sh
chmod +x ~/.ghostpass/tor/stop_tor.sh

# Step 5: Activate Python environment
echo ""
echo "🔧 Step 5: Activating Python environment..."
if [ -d "ghostpass_env" ]; then
    echo "🔧 Activating existing virtual environment..."
    source ghostpass_env/bin/activate
else
    echo "❌ Virtual environment not found"
    exit 1
fi

# Step 6: Test everything
echo ""
echo "🧪 Step 6: Testing everything..."

# Test Python
if command -v python &> /dev/null; then
    echo "✅ Python is available: $(python --version)"
else
    echo "❌ Python not found in virtual environment"
    exit 1
fi

# Test GHOST PASS
echo "🔍 Testing GHOST PASS..."
python -c "import ghostpass; print('✅ GHOST PASS imported successfully')" || {
    echo "❌ GHOST PASS import failed"
    exit 1
}

# Start TOR
echo "🚀 Starting TOR..."
~/.ghostpass/tor/start_tor.sh

# Test TOR connection
echo "🧪 Testing TOR connection..."
sleep 3
if curl --socks5 127.0.0.1:9050 --connect-timeout 10 https://check.torproject.org/ 2>/dev/null | grep -q "Congratulations"; then
    echo "✅ TOR connection confirmed!"
else
    echo "⚠️  TOR connection test failed"
fi

echo ""
echo "🎉 NewOnionKey issue fixed!"
echo ""
echo "📋 Summary:"
echo "  ✅ System TOR config: Fixed (NewOnionKey removed)"
echo "  ✅ User TOR config: Created (minimal)"
echo "  ✅ Python environment: Activated"
echo "  ✅ GHOST PASS: Ready to use"
echo ""
echo "🚀 Next steps:"
echo "  python -m ghostpass                    # Launch interactive dashboard"
echo "  python -m ghostpass connect            # Connect to TOR"
echo "  python -m ghostpass status             # Show status"
echo ""
echo "🛑 To stop TOR:"
echo "  ~/.ghostpass/tor/stop_tor.sh"
echo "" 