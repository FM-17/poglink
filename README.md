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

## Running the bot
There are a few different ways to run this bot on your own machine. Either in your own Python environment or in a docker container.

### Running in Python
To run the bot in Python you can either:
1. Execute via the CLI entrypoint: `ark-discord-bot`, passing config parameters any of the ways described below; or
2. Import within your own Python code and execute `ark_discord_bot.main.run`, passing in configuration parameters as keyword arguments.

### Running in Docker / Docker Compose
To run in a container, you can simply execute `docker run fm17/ark-discord-bot`, passing in any relevant configuration parameters as environment variables. In order to pass in a configuration file
or to maintain persistent data between containers mount a volume to the `/data` dir inside the container (or whichever data directory is configured via the `--data-dir` CLI argument or the `BOT_DATA_DIR`
environment variable).

Example `docker-compose.yaml`
```yaml
version: "3"
services:
  bot:
    image: fm17/ark-discord-bot:latest
    container_name: ark-discord-bot
    volumes:
      - ~/.ark-discord-bot:/custom-data-dir
    command: "" # provide CLI args here
    environment:
      BOT_DATA_DIR: "/custom-data-dir"
    networks:
      - bot-net

networks:
  bot-net:
```

## Configuration
This bot can pull configuration from one of multiple locations. Each parameter will be parsed independently in the following order of precedence:
1. CLI arguments
    - See help menu by running `ark-discord-bot -h` for more information.
2. Configuration File
    - Assumed to be named `config.yaml` within the data directory.
    - Data directory is set to `~/.ark-discord-bot` unless otherwise specified.
3. Environment variables
    - Each parameter can be set via an environment variable prefixed with `BOT_`.
    - E.g. to configure the bot's polling delay, set `BOT_POLLING_DELAY`.
4. Defaults (optional)
    - Some configuration parameters have default values assigned, which will be used
    in the absense of any other user-provided configuration values. 


### Parameter Summary
The following configuration parameters are available to be set in any of the above described methods:

| CLI Argument           | Env Var                | Default                                   | Required | Description     |
| ---------------------- | ---------------------- | ----------------------------------------- | -------- | --------------- |
| `--allowed-roles`      | `BOT_ALLOWED_ROLES`    | None                                      | No       | \<insert desc\> |
| `--polling-delay`      | `BOT_POLLING_DELAY`    | 60                                        | No       | \<insert desc\> |
| `--rates-url`          | `BOT_RATES_URL`        | http://arkdedicated.com/dynamicconfig.ini | No       | \<insert desc\> |
| `--bans-url`           | `BOT_BANS_URL`         | http://arkdedicated.com/bansummary.txt    | No       | \<insert desc\> |
| `--rates-channel-id`   | `BOT_RATES_CHANNEL_ID` | None                                      | Yes      | \<insert desc\> |
| `--bans-channel-id`    | `BOT_BANS_CHANNEL_ID`  | None                                      | Yes      | \<insert desc\> |
| `--token `             | `BOT_TOKEN`            | None                                      | Yes      | \<insert desc\> | 
| `--data-dir`           | `BOT_DATA_DIR`         | ~/.ark-discord-bot                        | No       | \<insert desc\> |
| `--debug`              | `BOT_DEBUG`            | False                                     | No       | \<insert desc\> |
    
## Developing

### Formatting
Project is formatted with `black==20.8b1` ([link](https://pypi.org/project/black/))

### Testing
Run tests with `pytest` ([link](https://docs.pytest.org/en/6.2.x/)) after installing requirements via `pip install -r requirements.dev.txt`.

## Future Updates
- [ ] Editable embeds
- [ ] Auto-publishing in announcement channels
- [ ] In-game server notifications posted to Discord channels

*Initially developed for use in the official ARK: Survival Evolved Discord server*
