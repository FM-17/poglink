#!/bin/bash

if touch $DATA_DIR 2> /dev/null; then
    ark-discord-bot $@
else 
    echo "No data directory defined. Creating "
    mkdir ~/.ark-discord-bot
    exit 1
fi 

mkdir ~./ark-discord-bot
cp sample-config.yaml