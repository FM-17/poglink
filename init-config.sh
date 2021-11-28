#!/bin/bash

DEFAULT_DIR="${HOME}/.ark-discord-bot"

# Check if user set custom config dir; if not, use default
if [ -z "${BOT_CONFIG_DIR}" ]; then 
    echo "BOT_CONFIG_DIR not set; Assuming default location ${DEFAULT_DIR}"
    BOT_CONFIG_DIR="${DEFAULT_DIR}"
else
    echo "Using custom config dir: BOT_CONFIG_DIR=${BOT_CONFIG_DIR}"
fi

# Check if config dir exists; if not, create it
if [ ! -d "${BOT_CONFIG_DIR}" ]; then
    echo "Directory ${BOT_CONFIG_DIR} doesn't exist; Creating."
    mkdir -p "${BOT_CONFIG_DIR}"
else   
    echo "Directory exists: ${BOT_CONFIG_DIR}. Skipping creation."
fi