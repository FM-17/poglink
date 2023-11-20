## Configuration
This bot can pull configuration from one of multiple locations. Each parameter will be parsed independently in the following order of precedence:
1. CLI arguments
    - See help menu by running `poglink -h` for more information.
2. Configuration File
    - Assumed to be named `config.yaml` within the data directory.
    - Data directory is set to `~/.poglink` when running natively unless otherwise specified. See [Docker Instructions](https://github.com/FM-17/poglink/blob/main/docs/docker-installation.md) for more information on how to configure this directory as a bind-mount.
    - See the supplied [sample configuration file](https://github.com/FM-17/poglink/blob/main/sample-config.yaml) for a reference of how to set parameters in this way.
3. Environment variables
    - Each parameter can be set via an environment variable prefixed with `BOT_`, in ALL CAPS.
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
| `--rates-urls`         | `BOT_RATES_URLS`         | [{"server_name": "Official","url": "https://cdn2.arkdedicated.com/asa/dynamicconfig.ini","color": "0x63BCC3",}] | Yes       | API URL to check for server rates (dict containing server title, url, and embed color)        |
| `--bans-url`           | `BOT_BANS_URL`           | http://arkdedicated.com/bansummary.txt    | No       | 🚧 [WIP] API URL to check for a ban summary                              |
| `--rates-channel-id`   | `BOT_RATES_CHANNEL_ID`   | None                                      | Yes      | Channel ID to post rates in                                          |
| `--bans-channel-id`    | `BOT_BANS_CHANNEL_ID`    | None                                      | Yes      | 🚧 [WIP] Channel ID to post ban summary in  WIP                                   |
| `--token `             | `BOT_TOKEN`              | None                                      | Yes      | Bot token (from Discord Developer Portal)                            |
| `--data-dir`           | `BOT_DATA_DIR`           | ~/.poglink                        | No       | Directory that will contain bot data, such as the `config.yaml` file |
| `--debug`              | `BOT_DEBUG`              | False                                     | No       | Enables debug logging |
| `--send-embed-on-startup` | `BOT_SEND_EMBED_ON_STARTUP`| False                                | No       | Send embed containing current rates found after starting the bot for the first time. | 

## Configuration Examples
- - - 
**Example 1:** Running Poglink to monitor rates on Official PC and Smalltribes servers

### Using `config.yaml`
```yaml
# REQUIRED 
token: JIMyUDY3Lah3SDd5JAM3Xds1.UH15df.lgOyDi5al5D_7d21gDDkAdHdlT3 # fake token
rates_channel_id: 733415533152301503 

rates_urls: 
- server_name: Official
  url:  https://cdn2.arkdedicated.com/asa/dynamicconfig.ini
  color: 0x63BCC3
- server_name: Smalltribes
  url: https://cdn2.arkdedicated.com/asa/smalltribes_dynamicconfig.ini
  color: 0xF8DE74
```

- - - 
**Example 2:** Running Poglink from a custom data directory

### Using `config.yaml` 

> ⚠ You cannot set a custom data directory solely from the `config.yaml` file because the bot requires the data directory location in order to find the `config.yaml` file.

### Using the CLI
```bash
poglink --data-dir=~/custom_data_dir
```
