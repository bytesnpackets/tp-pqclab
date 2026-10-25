#!/bin/bash
echo "========================================"
echo "   PQCLab: Linux Auto-Installer"
echo "========================================"

# 1. Install System Dependencies
echo "[1/4] Installing dependencies (requires sudo)..."
sudo apt-get update
sudo apt-get install -y build-essential git cmake libssl-dev python3-venv python3-tk

# 2. Create Venv
echo "[2/4] Creating Virtual Environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "      (venv created)"
else
    echo "      (venv exists, skipping)"
fi

# 3. Install liboqs
echo "[3/4] Building liboqs (This takes 2-3 mins)..."
source venv/bin/activate

if pip show oqs > /dev/null; then
    echo "      (liboqs is already installed!)"
else
    git clone https://github.com/open-quantum-safe/liboqs-python.git _install_temp
    cd _install_temp
    pip install .
    cd ..
    rm -rf _install_temp
    echo "      (Build complete!)"
fi

echo "========================================"
echo "   SETUP COMPLETE! Run: ./run.sh"
echo "========================================"