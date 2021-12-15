#!/bin/bash
set -e 

# Define data directory to be used for application config file.
DATA_DIR=${DATA_DIR:-${HOME}/.poglink}

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
    echo -e "\n\nVirtual environment not detected."
    PYTHON_EXECUTABLE="$(which python3)"
else 
    echo -e "\n\nVirtual environment detected."
    PYTHON_EXECUTABLE="${VIRTUAL_ENV}/bin/python3"
fi 

echo "Configuring service to run with ${PYTHON_EXECUTABLE}"

# Disable service if currently running from a previous installation
SERVICE_FILE_PATH=/etc/systemd/system/poglink.service
sudo systemctl stop "$SERVICE_FILE_PATH" || true

# Copy service file into place
sudo install \
    -v \
    --backup \
    --suffix .bak \
    ../resources/poglink.service \
    ${SERVICE_FILE_PATH}

# Replace values in service file
sudo sed -i "s@\#\#PYTHON\#\#@${PYTHON_EXECUTABLE}@g" "${SERVICE_FILE_PATH}"
sudo sed -i "s@\#\#DATA_DIR\#\#@${DATA_DIR}@g" "${SERVICE_FILE_PATH}"
sudo sed -i "s@\#\#USER\#\#@${USER}@g" "${SERVICE_FILE_PATH}"

# Copy sample config to ${DATA_DIR} if it doesn't exist yet
if [ ! -e ${DATA_DIR}/config.yaml ]; then  
    echo "Poglink config not found in $DATA_DIR; Using creating from sample..."
    mkdir -p ${DATA_DIR}
    cp ../sample-config.yaml ${DATA_DIR}/config.yaml

    echo -e "\n\nIMPORTANT!!! A sample configuration file has been created at ${DATA_DIR}/config.yaml . Please edit this file before starting the application for the first time."
fi

# Reload systemd daemon
sudo systemctl daemon-reload 

# Enable service
sudo systemctl enable poglink 

echo -e "\n\nThe Poglink service has been enabled to start at boot." 
echo "Start the service now by running 'sudo systemctl start poglink'."
echo "Monitor logs via 'journalctl -fu poglink'."
echo "To stop the service, run `sudo systemctl stop poglink`. To prevent from starting at boot, run `sudo systemctl disable poglink`."
