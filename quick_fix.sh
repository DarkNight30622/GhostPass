#!/bin/bash

# Quick Fix Script for GHOST PASS Installation Issues
# This script addresses the specific errors you encountered

echo "🔧 Quick Fix for GHOST PASS Installation Issues"
echo "================================================"

# Check if we're in the right directory
if [ ! -f "setup.py" ] || [ ! -f "requirements.txt" ]; then
    echo "❌ Error: setup.py or requirements.txt not found"
    echo "Make sure you're in the ghostpass directory"
    exit 1
fi

echo "✅ Found setup.py and requirements.txt"

# Check if virtual environment exists and activate it
if [ -d "ghostpass_env" ]; then
    echo "🔧 Activating existing virtual environment..."
    source ghostpass_env/bin/activate
else
    echo "❌ Virtual environment not found. Creating new one..."
    python3 -m venv ghostpass_env
    source ghostpass_env/bin/activate
fi

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Install the package
echo "🔧 Installing GHOST PASS in development mode..."
pip install -e .

echo ""
echo "✅ Quick fix completed!"
echo ""
echo "📋 Test the installation:"
echo "  python -m ghostpass --help"
echo ""
echo "🚀 Run GHOST PASS:"
echo "  python -m ghostpass"
echo "" 