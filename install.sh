#!/bin/bash

echo "Setting up HamAlert Client..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv hamalert_env

# Activate virtual environment
echo "Activating virtual environment..."
source hamalert_env/bin/activate

# Install the package (and setuptools for editable installs)
echo "Installing package..."
pip install -q setuptools
pip install -e . -q

# Collect user credentials
echo ""
read -rp "Enter your HamAlert callsign: " CALLSIGN
read -rsp "Enter your HamAlert password: " PASSWORD
echo ""

# Write user config file
CONFIG_DIR="${HOME}/.hamalert"
CONFIG_FILE="${CONFIG_DIR}/config.json"
mkdir -p "${CONFIG_DIR}"
cat > "${CONFIG_FILE}" <<EOF
{
    "host": "hamalert.org",
    "port": 7300,
    "callsign": "${CALLSIGN}",
    "password": "${PASSWORD}",
    "timeout": 30
}
EOF
chmod 600 "${CONFIG_FILE}"

echo ""
echo "Setup complete! Config saved to ${CONFIG_FILE}"
echo ""
echo "To run HamAlert:"
echo "  source hamalert_env/bin/activate && python src/main.py"