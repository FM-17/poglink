#!/bin/bash

# Change directory to current script dir to ensure init-config.sh script is found.
cd "$(dirname "$(realpath "$0")")";

# Run config dir initialization (in current shell to make BOT_DATA_DIR variable active)
source ./init-config.sh

# Run container as defined in compose file
docker-compose up bot