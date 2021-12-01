This bot monitors the ARK Web API and posts changes to Discord.

![image](https://user-images.githubusercontent.com/82160306/143663008-ae44ae7a-4499-4abe-9568-89109f390128.png)

## Requirements
- Python 3.6.9
- [pip](https://pip.pypa.io/en/latest/installation/)
- [optional] A virtual environment manager such as [pyenv](https://github.com/pyenv/pyenv) or [virtualenv](https://virtualenv.pypa.io/en/latest/)

## Prerequisites
1. Create a bot on the [Discord Developer Portal](https://discordapp.com/developers/)
2. Turn on **Message Content Intent** in the bot's settings page on the developer portal
3. Create Bot URL via URL Generator in the Discord Developer Portal. Make sure the bot has `Send Messages`, `Read Messages/View Channels`, `Read Message History` and `Embed Links` permissions.
4. Invite the bot to the server

## Setup 
This bot can either run natively or from within a docker container. 
- [Instructions for running natively](docs/setup/native.md)
- [Instructions for running within Docker](docs/setup/docker.md)
    
## Future Updates
- [ ] Editable embeds
- [ ] Auto-publishing in announcement channels
- [ ] In-game server notifications posted to Discord channels

*Initially developed for use in the official ARK: Survival Evolved Discord server*
