#!/bin/bash

if touch $BOT_OUTPUT_DIR 2> /dev/null; then
    ark-discord-bot $@
else 
    echo "Cannot write to data directory: ${BOT_OUTPUT_DIR}. Create data directory on host before running container."
    exit 1
fi 