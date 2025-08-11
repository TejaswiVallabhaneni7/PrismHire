#!/usr/bin/env bash
set -e  # Exit on error

echo "🔹 Starting PrismHire Dev Container setup..."

# Set Python interpreter path
PYTHON_BIN="/usr/local/bin/python3"

# Create virtual environment only if not exists
if [ ! -d ".venv" ]; then
    echo "🔹 Creating Python virtual environment..."
    $PYTHON_BIN -m venv .venv
else
    echo "✅ Virtual environment already exists. Skipping creation."
fi

# Activate venv
source .venv/bin/activate

# Upgrade pip, setuptools, and wheel
echo "🔹 Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel

# Install requirements.txt if exists
if [ -f "requirements.txt" ]; then
    echo "🔹 Installing requirements from requirements.txt..."
    pip install --no-cache-dir -r requirements.txt
else
    echo "⚠️ No requirements.txt found. Skipping package installation."
fi

# Confirm setup
echo "✅ PrismHire development environment is ready."
