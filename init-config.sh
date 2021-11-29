#!/bin/bash

DEFAULT_DIR="${HOME}/.ark-discord-bot"

# Check if user set custom config dir; if not, use default
if [ -z "${BOT_DATA_DIR}" ]; then 
    echo "BOT_DATA_DIR not set; Assuming default location ${DEFAULT_DIR}"
    BOT_DATA_DIR="${DEFAULT_DIR}"
else
    echo "Using custom config dir: BOT_DATA_DIR=${BOT_DATA_DIR}"
fi

# Check if config dir exists; if not, create it
if [ ! -d "${BOT_DATA_DIR}" ]; then
    echo "Directory ${BOT_DATA_DIR} doesn't exist; Creating."
    mkdir -p "${BOT_DATA_DIR}"
else   
    echo "Directory exists: ${BOT_DATA_DIR}. Skipping creation."
fi