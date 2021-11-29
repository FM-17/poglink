#!/bin/bash

# Check that directory exists
if [ -d "${BOT_OUTPUT_DIR}" ]; then
    # Check that directory is writeable
    if [ ! -w "${BOT_OUTPUT_DIR}" ]; then
        echo "Cannot write to data directory: ${BOT_OUTPUT_DIR}. Create or set write permissions for data directory on host before running container."
    fi 
else 
    # Create directory
    echo "Data directory ${BOT_OUTPUT_DIR} doesn't exist; Creating."
    mkdir -p "${BOT_OUTPUT_DIR}"
fi

# Check if data directory contains a config file; if not, copy the sample
CONFIG_FILE="${BOT_OUTPUT_DIR}/config.yaml"
if [ ! -e "${CONFIG_FILE}" ]; then
    echo "No config file found in data directory; Creating a sample."
    cp /sample_config.yaml "${CONFIG_FILE}"
fi
