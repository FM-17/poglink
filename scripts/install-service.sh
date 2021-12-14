#!/bin/bash
set -e 

# Change to script directory for predictable behaviour
cd "$(dirname "$0")"

# Check whether virtual environment is active
if [ -z "${VIRTUAL_ENV}" ] && [ "${FORCE}" != "true"  ]; then
    echo "Warning: Virtual environment not detected! It is highly recommended to install this program to run under a virtual environment. Please activate your virtual environment and run this script again."
    echo "If you're certain you'd like to continue without a virtual environment, you can run again with 'FORCE=true'." 
    exit 1
fi

# Install poglink python package
pip install poglink

# Obtain path to python executable
if [ -z "${VIRTUAL_ENV}" ]; then
    PYTHON_EXECUTABLE="$(which python3)"
else 
    PYTHON_EXECUTABLE="${VIRTUAL_ENV}/bin/python3"
fi 

echo "Configuring service to run with ${PYTHON_EXECUTABLE}"

# Copy service file into place
OUTPUT_PATH=/etc/systemd/system/poglink.service

sudo install \
    -v \
    --backup \
    --suffix .bak \
    ../resources/poglink.service \
    ${OUTPUT_PATH}

# TODO: Copy sample config to ~/.poglink if it doesn't exist yet

# Replace python executable text in service file
sudo sed -i "s@\#\#PYTHON\#\#@${PYTHON_EXECUTABLE}@g" "${OUTPUT_PATH}"

# Reload systemd daemon
sudo systemctl daemon-reload 

# Enable service
sudo systemctl enable poglink 

echo "Start service by running 'sudo systemctl start poglink'. Monitor logs via 'journalctl -fu poglink'."
    