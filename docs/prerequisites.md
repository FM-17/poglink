
# Prerequisites
## Install dependencies

- Python 3.7+
- pip

## Create the bot

This bot runs on your own machine or server. You'll need to create the bot on the Discord Developer Portal and invite it to your Discord server before you can run it.
1. Create a bot on the [Discord Developer Portal](https://discordapp.com/developers/)
2. Enable **Message Content Intent** from the Bot tab. 
3. Navigate to **OAuth2 > URL Generator** Make sure the bot has `Send Messages`, `Read Messages/View Channels`, `Read Message History` and `Embed Links` permissions.
4. Invite the bot to the server

## Prepare data directory and config file

The recommended approach to setting configuration values is through a configuration file. The following instructions will guide you to running the bot for the first time, using file-based configuration.

By default, this bot will save all data to `~/.poglink`, but you can choose a different directory if you'd like (see [Configuration](https://github.com/FM-17/poglink/blob/main/docs/configuration.md)). 

**Note:** This bot will always save its data (cached server statuses) to the same directory as the config file, as these locations are both controlled via the `data_dir` parameter.

1. Create the data directory if it doesn't already exist, for example
  
    ```bash
    mkdir ~/.poglink # creates data directory (~/.poglink by default)
    ```

2. Create a `config.yaml` file in your data directory

    ```bash
    cd ~/.poglink # navigates to data directory (~/.poglink by default)
    touch config.yaml # creates empty config file
    ```

3. Copy the contents of [sample_config.yaml](https://github.com/FM-17/poglink/blob/main/sample-config.yaml) into your `config.yaml` file and configure all **required** parameters. See [Configuration](https://github.com/FM-17/poglink/blob/main/docs/configuration.md) for more details.

## Next steps
You're now ready to install and run the bot. There are a number of ways to do this. Pick your favourite.

- [Running natively in Python](https://github.com/FM-17/poglink/blob/main/docs/native-installation.md)
- [Running within Docker container](https://github.com/FM-17/poglink/blob/main/docs/docker-installation.md)
