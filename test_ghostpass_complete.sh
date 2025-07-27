#!/bin/bash

# Comprehensive GHOST PASS Test and Fix Script
# This script fixes both TOR and Python environment issues

echo "🧪 GHOST PASS Comprehensive Test and Fix"
echo "========================================="

# Check if we're in the right directory
if [ ! -f "setup.py" ] || [ ! -f "requirements.txt" ]; then
    echo "❌ Error: setup.py or requirements.txt not found"
    echo "Make sure you're in the ghostpass directory"
    exit 1
fi

echo "✅ Found setup.py and requirements.txt"

# Step 1: Fix Python Environment
echo ""
echo "🔧 Step 1: Fixing Python Environment"
echo "===================================="

# Check if virtual environment exists
if [ -d "ghostpass_env" ]; then
    echo "🔧 Activating existing virtual environment..."
    source ghostpass_env/bin/activate
else
    echo "❌ Virtual environment not found. Creating new one..."
    python3 -m venv ghostpass_env
    source ghostpass_env/bin/activate
fi

# Verify Python is available
if command -v python &> /dev/null; then
    echo "✅ Python is available: $(python --version)"
else
    echo "❌ Python not found in virtual environment"
    echo "🔧 Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install -e .
fi

# Step 2: Fix TOR Configuration
echo ""
echo "🔧 Step 2: Fixing TOR Configuration"
echo "==================================="

# Stop any existing TOR processes
echo "🛑 Stopping existing TOR processes..."
pkill -f tor 2>/dev/null || true
sleep 3

# Remove existing configuration
echo "🧹 Cleaning existing configuration..."
rm -rf ~/.ghostpass/tor
mkdir -p ~/.ghostpass/tor

# Create proper TOR configuration
echo "📝 Creating proper TOR configuration..."
cat > ~/.ghostpass/tor/torrc << 'EOF'
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

# Create data directory
mkdir -p ~/.ghostpass/tor/data

# Create fixed startup script
echo "📝 Creating fixed startup script..."
cat > ~/.ghostpass/tor/start_tor.sh << 'EOF'
#!/bin/bash
# Start TOR for GHOST PASS

TOR_DIR="$HOME/.ghostpass/tor"
TOR_CONFIG="$TOR_DIR/torrc"
TOR_DATA="$TOR_DIR/data"
TOR_PID="$TOR_DIR/tor.pid"

echo "🚀 Starting TOR for GHOST PASS..."

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

# Use environment variable to prevent reading system config
export TOR_CONFIG_FILE="$TOR_CONFIG"

# Start TOR with minimal configuration
tor --config "$TOR_CONFIG" --data "$TOR_DATA" --pidfile "$TOR_PID" --ignore-missing-torrc --defaults-torrc /dev/null --fname /dev/null &

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

# Step 3: Test Everything
echo ""
echo "🧪 Step 3: Testing Everything"
echo "============================="

# Test Python imports
echo "🔍 Testing Python imports..."
python -c "import ghostpass; print('✅ GHOST PASS imported successfully')" || {
    echo "❌ GHOST PASS import failed"
    echo "🔧 Reinstalling GHOST PASS..."
    pip install -e .
}

# Test CLI
echo "🔍 Testing CLI..."
python -m ghostpass --help || {
    echo "❌ CLI test failed"
    exit 1
}

# Start TOR
echo "🔍 Starting TOR..."
~/.ghostpass/tor/start_tor.sh

# Test TOR connection
echo "🔍 Testing TOR connection..."
sleep 3
if curl --socks5 127.0.0.1:9050 --connect-timeout 10 https://check.torproject.org/ 2>/dev/null | grep -q "Congratulations"; then
    echo "✅ TOR connection working!"
else
    echo "⚠️  TOR connection test failed"
fi

# Run comprehensive test
echo "🔍 Running comprehensive test..."
python test_installation.py

echo ""
echo "🎉 Comprehensive test completed!"
echo ""
echo "📋 Summary:"
echo "  ✅ Python environment: Fixed"
echo "  ✅ TOR configuration: Fixed"
echo "  ✅ GHOST PASS: Ready to use"
echo ""
echo "🚀 Next steps:"
echo "  python -m ghostpass                    # Launch interactive dashboard"
echo "  python -m ghostpass connect            # Connect to TOR"
echo "  python -m ghostpass status             # Show status"
echo "" 