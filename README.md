## Requirements
- `python 3.6.9`+ 
- [pip package manager](https://pip.pypa.io/en/latest/installation/) v21+ 
- [virtualenv](https://virtualenv.pypa.io/en/latest/)

## Prerequisites
1. Create a bot on the [Discord Developer Portal](https://discordapp.com/developers/)
2. Turn on **Message Content Intent** in the bot's settings page on the developer portal
3. Create Bot URL via URL Generator in the Discord Developer Portal. Make sure the bot has `Send Messages`, `Read Messages/View Channels`, `Read Message History` and `Embed Links` permissions.
4. Invite the bot to the server

## Setup
The following can be done on your local machine, a VPS, etc. These guide assumes it will be running on a linux machine.

1. Download the bot
    Option A: Download and extract the [latest bot release](https://github.com/FM-17/ark_discord_bot/releases/latest) 
    Option B: Clone the repo via `git clone git@github.com:FM-17/ark_discord_bot.git` 
2. Rename `config_template.yaml` to `config.yaml` and copy it into the `/local` directory
3. Open `config.yaml` and fill in the required values.
4. Navigate to the `ark_discord_bot/` directory
5. Run `setup.sh`

