

## Prerequisites
1. Create a bot on the [Discord Developer Portal](https://discordapp.com/developers/)
2. Turn on **Message Content Intent** in the bot's settings page on the developer portal
3. Create Bot URL via URL Generator in the Discord Developer Portal. Make sure the bot has `Send Messages`, `Read Messages/View Channels`, `Read Message History` and `Embed Links` permissions.
4. Invite the bot to the server

## Setup
The following can be done on your local machine, a VPS, etc. These instructions assume it will be running on a linux machine.
1. [Download the latest bot release here](https://github.com/FM-17/ark_discord_bot/releases/latest) (click on "Source code (zip)") or `git clone `
2. Extract the downloaded zip file to a new folder
3. Copy `config_template.yaml` to `local/` and rename the copy to `config.yaml`
4. Open `config.yaml` and fill in the required values.
