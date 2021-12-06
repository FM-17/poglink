This bot monitors the ARK Web API and posts changes to Discord.

![image](https://user-images.githubusercontent.com/82160306/143663008-ae44ae7a-4499-4abe-9568-89109f390128.png)

## Requirements
- Python 3.7+
- [pip](https://pip.pypa.io/en/latest/installation/)

## Prerequisites
1. Create a bot on the [Discord Developer Portal](https://discordapp.com/developers/)
2. Turn on **Message Content Intent** in the bot's settings page on the developer portal
3. Create Bot URL via URL Generator in the Discord Developer Portal. Make sure the bot has `Send Messages`, `Read Messages/View Channels`, `Read Message History` and `Embed Links` permissions.
4. Invite the bot to the server

## Installation and Usage
There are a few different ways to run this bot on your own machine. Either in your own Python environment or in a docker container.

### Installing in Python
1. Get the code via either of the following two methods:

    a) Download & extract the [latest bot release](https://github.com/FM-17/ark_discord_bot/releases/latest)

    b) Clone the repo via `git clone https://github.com/FM-17/ark_discord_bot.git` 

2. Copy `sample_config.yaml`, rename it to `config.yaml`, and fill in the required values.
3. Install the bot
    
    I'd suggest doing this within a virtual environment via [pyenv](https://github.com/pyenv/pyenv) or [virtualenv](https://pypi.org/project/virtualenv/), but its not required.
    ```bash
    cd {download location}/ark-discord-bot/
    pip install .
    ```

### Running in Python
To run the bot in Python you can either:
1. Execute via the CLI entrypoint: `ark-discord-bot`, passing config parameters any of the ways described below; or
2. Import within your own Python code and execute `ark_discord_bot.main.run`, passing in configuration parameters as keyword arguments.

### Installing in Docker
`WIP`
  
### Running in Docker / Docker Compose
To run in a container, you can simply execute `docker run fm17/ark-discord-bot`, passing in any relevant configuration parameters as environment variables. In order to pass in a configuration file or to maintain persistent data between containers, mount a volume to the `/data` dir inside the container (or whichever data directory is configured via the `--data-dir` CLI argument or the `BOT_DATA_DIR` environment variable). Sim

In the example below, the host's `~/.ark-discord-bot` directory has been mounted to the container's `/data` directory. Therefore the `config.yaml` file must be moved to the `~/.ark-discord-bot` directory in order to be passed into the container. Both of these mounting directories can be modified as needed, see [Configuration](#configuration) for more details.

Example `docker-compose.yaml`
```yaml
version: "3"
services:
  bot:
    image: fm17/ark-discord-bot:latest
    container_name: ark-discord-bot
    volumes:
      - ~/.ark-discord-bot:/data
    command: "" # provide CLI args here
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
    in the absence of any other user-provided configuration values. 


### Parameter Summary
The following configuration parameters are available to be set in any of the above described methods:

| CLI Argument           | Env Var                  | Default                                   | Required | Description     |
| ---------------------- | ------------------------ | ----------------------------------------- | -------- | --------------- |
| `--allowed-roles`      | `BOT_ALLOWED_ROLES`      | None                                      | No       | Roles permitted to use bot commands |
| `--polling-delay`      | `BOT_POLLING_DELAY`      | 60                                        | No       | Delay between each API check |
| ``--rates-url``        | ``BOT_RATES_URL``        | http://arkdedicated.com/dynamicconfig.ini | No       | API endpoint to check for server rates |
| ``--bans-url``         | ``BOT_BANS_URL``         | http://arkdedicated.com/bansummary.txt    | No       | API endpoint to check for a ban summary |
| ``--rates-channel-id`` | ``BOT_RATES_CHANNEL_ID`` | None                                      | Yes      | Channel ID to post rates in |
| ``--bans-channel-id``  | ``BOT_BANS_CHANNEL_ID``  | None                                      | Yes      | Channel ID to post ban summary in |
| ``--token ``           | ``BOT_TOKEN``            | None                                      | Yes      | Bot token (from Discord Developer Portal) |
| ``--data-dir``         | ``BOT_DATA_DIR``         | ~/.ark-discord-bot                        | No       | Directory that will contain bot data, such as the `config.yaml` file |
| ``--debug``            | ``BOT_DEBUG``            | False                                     | No       | Enables debug logging |

### Developer TODOs
#### Deployment
- [ ] Set up `semantic-release` for automatically versioning and tagging from commit messages
- [ ] Set up `setuptools_scm` to automatically version the python package from git tags
- [ ] Set up `twine publish` command in Makefile, and include in requirements.dev.txt 
- [ ] Rename bot and refactor
- [ ] Add to pypi
- [ ] Add [[Github Actions]] for pypi
- [ ] Add [[Github Actions]] for [docker hub](https://medium.com/rockedscience/docker-ci-cd-pipeline-with-github-actions-6d4cd1731030)
- [ ] Add docs to DockerHub (even just a backlink to github would do)

#### Bot Development
- [ ] Rework `rates.py` to make use of RatesStatus and RatesDiff
- [ ] Add emojis to rates embeds
- [ ] Add docs explaining current auto-publishing functionality
- [ ] Add more debugging code
- [x] Auto-publishing in announcement channels

#### Low Priority / Next Release
- [ ] Add ability to post other server rates. Rather than just using the `dynamicconfig.ini` endpoint, perhaps add a parameter that takes in a list of endpoints, ex. `["pc_smalltribes_dynamicconfig.ini", "xbox_smalltribes_dynamiconfig.ini"]`. Alternatively, combine all rates into a table that gets added to the embed.
- [ ] Rework bans.py to make use of bans models
- [ ] Reformat ban summary output
- [ ] Make `bans.py` edit the embed rather than sending a new one
- [ ] Add auto-publish/no publish as a parameter for each cog, perhaps `auto-publish-channels = [<chan_ID1>, <chan_ID1>]`
- [ ] In-game server notifications posted to Discord channels
- [ ] Convert to use `setup.cfg` instead of `setup.py`

*Initially developed for use in the official ARK: Survival Evolved Discord server*
