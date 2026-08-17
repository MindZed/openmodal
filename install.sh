#!/bin/bash
echo "🔥 Mindzed Technologies Setup Launcher 🔥"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for Python 3
if command_exists python3; then
    PYTHON_CMD="python3"
elif command_exists python; then
    PYTHON_CMD="python"
else
    echo "[!] Python is not installed."
    read -p "? Do you want to automatically install Python? (y/n): " install_choice
    if [[ "$install_choice" == "y" || "$install_choice" == "Y" ]]; then
        if [ "$(uname)" == "Darwin" ]; then
            echo "=> macOS detected. Installing via Homebrew..."
            if ! command_exists brew; then
                echo "=> Homebrew not found. Installing Homebrew first..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            brew install python
        elif command_exists apt-get; then
            echo "=> Debian/Ubuntu detected. Installing via apt-get..."
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv
        elif command_exists yum; then
            echo "=> CentOS/RHEL detected. Installing via yum..."
            sudo yum install -y python3 python3-pip
        else
            echo "[-] Unsupported OS for automatic installation. Please install Python manually from python.org"
            exit 1
        fi
        PYTHON_CMD="python3"
    else
        echo "Exiting. Please install Python to continue."
        exit 1
    fi
fi

echo "=> Python detected: $($PYTHON_CMD --version)"
echo "=> Launching Interactive Setup..."
$PYTHON_CMD setup.py
