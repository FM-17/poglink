This bot monitors the ARK Web API and posts changes to Discord.

![image](https://user-images.githubusercontent.com/82160306/145702199-a14a4469-76c5-49fd-b5e0-1f6eb197a1e4.png)

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

- Before installing, copy `sample_config.yaml`, rename it to `config.yaml`, and fill in the required values.

- You'll also need to decide where you want to store this configuration file. By default, the bot will look for it in `~/.poglink`, but you can change the location via the `-d` CLI argument. 

- Whether you decide to use the default location, or a custom one, you'll need to move the `config.yaml` file to that directory before running.

- For example, if you chose to use the default, you'd need to move the `config.yaml` file to `~/.poglink/config.yaml`

#### Installing from PyPi

Run the following command to install from PyPi

    pip install poglink
    
#### Installing from Git repo
1. Get the code via either of the following two methods:

    a) Download & extract the [latest bot release](https://github.com/FM-17/poglink/releases/latest)

    b) Clone the repo via `git clone https://github.com/FM-17/poglink.git` 

2. Install the bot
    
    I'd suggest doing this within a virtual environment via [pyenv](https://github.com/pyenv/pyenv) or [virtualenv](https://pypi.org/project/virtualenv/), but its not required.
    ```bash
    cd {download location}/poglink/
    pip install .
    ```

### Running in Python

To run the bot in Python you can either:
1. Execute via the CLI entrypoint: `poglink`, passing config parameters any of the ways described below; or
2. Import within your own Python code and execute `poglink.main.run`, passing in configuration parameters as keyword arguments.

### Installing in Docker
Run the following command to pull the latest docker image
```
docker pull fm17/poglink
```

### Running in Docker / Docker Compose
To run in a container, you can simply execute `docker run fm17/poglink`, passing in any relevant configuration parameters as environment variables. In order to pass in a configuration file or to maintain persistent data between containers, mount a volume to the `/data` dir inside the container (or whichever data directory is configured via the `--data-dir` CLI argument or the `BOT_DATA_DIR` environment variable). 

In the example below, the host's `~/.poglink` directory has been mounted to the container's `/data` directory. Therefore the `config.yaml` file must be moved to the `~/.poglink` directory in order to be passed into the container. Both of these mounting directories can be modified as needed, see [Configuration](#configuration) for more details.

Example `docker-compose.yaml`
```yaml
version: "3"
services:
  bot:
    image: fm17/poglink:latest
    container_name: poglink
    volumes:
      - ~/.poglink:/data
    command: "" # provide CLI args here
    networks:
      - bot-net

networks:
  bot-net:
```

## Configuration
This bot can pull configuration from one of multiple locations. Each parameter will be parsed independently in the following order of precedence:
1. CLI arguments
    - See help menu by running `poglink -h` for more information.
2. Configuration File
    - Assumed to be named `config.yaml` within the data directory.
    - Data directory is set to `~/.poglink` unless otherwise specified.
3. Environment variables
    - Each parameter can be set via an environment variable prefixed with `BOT_`.
    - E.g. to configure the bot's polling delay, set `BOT_POLLING_DELAY`.
4. Defaults (optional)
    - Some configuration parameters have default values assigned, which will be used
    in the absence of any other user-provided configuration values. 


### Parameter Summary
The following configuration parameters are available to be set in any of the above described methods:

| CLI Argument           | Env Var                  | Default                                   | Required | Description                                                          |
| ---------------------- | ------------------------ | ----------------------------------------- | -------- | -------------------------------------------------------------------- |
| `--allowed-roles`      | `BOT_ALLOWED_ROLES`      | None                                      | No       | Roles permitted to use bot commands (comma-separated list)           |
| `--polling-delay`      | `BOT_POLLING_DELAY`      | 60                                        | No       | Delay between each API check                                         |
| `--rates-urls`         | `BOT_RATES_URLS`         | http://arkdedicated.com/dynamicconfig.ini | No       | API endpoint to check for server rates (comma-separated list)        |
| `--bans-url`           | `BOT_BANS_URL`           | http://arkdedicated.com/bansummary.txt    | No       | API endpoint to check for a ban summary                              |
| `--rates-channel-id`   | `BOT_RATES_CHANNEL_ID`   | None                                      | Yes      | Channel ID to post rates in                                          |
| `--bans-channel-id`    | `BOT_BANS_CHANNEL_ID`    | None                                      | Yes      | Channel ID to post ban summary in                                    |
| `--token `             | `BOT_TOKEN`              | None                                      | Yes      | Bot token (from Discord Developer Portal)                            |
| `--data-dir`           | `BOT_DATA_DIR`           | ~/.poglink                        | No       | Directory that will contain bot data, such as the `config.yaml` file |
| `--debug`              | `BOT_DEBUG`              | False                                     | No       | Enables debug logging                                                |

 *Initially developed for use in the official ARK: Survival Evolved Discord*
