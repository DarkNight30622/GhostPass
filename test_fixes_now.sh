#!/bin/bash

# Quick Test for TOR Fixes
echo "🧪 Testing TOR Fixes Right Now"
echo "==============================="

# Test 1: Check if we can bypass system config
echo "🔍 Test 1: Checking system TOR config..."
if [ -f "/etc/tor/torrc" ]; then
    echo "⚠️  System TOR config found: /etc/tor/torrc"
    echo "📋 First few lines:"
    head -5 /etc/tor/torrc
else
    echo "✅ No system TOR config found"
fi

# Test 2: Try the enhanced fix
echo ""
echo "🔍 Test 2: Trying enhanced fix..."
chmod +x fix_tor_issue.sh
./fix_tor_issue.sh

# Test 3: Try to start TOR
echo ""
echo "🔍 Test 3: Starting TOR..."
~/.ghostpass/tor/start_tor.sh

# Test 4: Check if TOR is running
echo ""
echo "🔍 Test 4: Checking TOR status..."
sleep 3
if ps aux | grep -v grep | grep -q "tor.*~/.ghostpass/tor/torrc"; then
    echo "✅ TOR is running!"
    
    # Test connection
    echo "🧪 Testing TOR connection..."
    if curl --socks5 127.0.0.1:9050 --connect-timeout 10 https://check.torproject.org/ 2>/dev/null | grep -q "Congratulations"; then
        echo "🎉 SUCCESS! TOR is working!"
    else
        echo "⚠️  TOR started but connection test failed"
    fi
else
    echo "❌ TOR is not running"
    echo "🔍 Checking for errors..."
    tail -n 10 ~/.ghostpass/tor/data/tor.log 2>/dev/null || echo "No log file found"
fi

echo ""
echo "📊 Test Results Summary:"
echo "========================="
if ps aux | grep -v grep | grep -q "tor.*~/.ghostpass/tor/torrc"; then
    echo "✅ TOR Status: RUNNING"
else
    echo "❌ TOR Status: NOT RUNNING"
fi

if curl --socks5 127.0.0.1:9050 --connect-timeout 5 https://check.torproject.org/ 2>/dev/null | grep -q "Congratulations"; then
    echo "✅ TOR Connection: WORKING"
else
    echo "❌ TOR Connection: FAILED"
fi

echo ""
echo "🎯 Next Steps:"
if ps aux | grep -v grep | grep -q "tor.*~/.ghostpass/tor/torrc"; then
    echo "✅ TOR is working! You can now use GHOST PASS"
    echo "🚀 Try: python -m ghostpass"
else
    echo "❌ TOR still not working. Try the aggressive fix:"
    echo "   chmod +x fix_tor_aggressive.sh"
    echo "   ./fix_tor_aggressive.sh"
    echo "   ~/.ghostpass/tor/start_tor.sh"
fi 