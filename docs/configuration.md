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
| `--rates-urls`         | `BOT_RATES_URLS`         | http://arkdedicated.com/dynamicconfig.ini | No       | API URL to check for server rates (comma-separated list)        |
| `--bans-url`           | `BOT_BANS_URL`           | http://arkdedicated.com/bansummary.txt    | No       | 🚧 [WIP] API URL to check for a ban summary                              |
| `--rates-channel-id`   | `BOT_RATES_CHANNEL_ID`   | None                                      | Yes      | Channel ID to post rates in                                          |
| `--bans-channel-id`    | `BOT_BANS_CHANNEL_ID`    | None                                      | Yes      | 🚧 [WIP] Channel ID to post ban summary in  WIP                                   |
| `--token `             | `BOT_TOKEN`              | None                                      | Yes      | Bot token (from Discord Developer Portal)                            |
| `--data-dir`           | `BOT_DATA_DIR`           | ~/.poglink                        | No       | Directory that will contain bot data, such as the `config.yaml` file |
| `--debug`              | `BOT_DEBUG`              | False                                     | No       | Enables debug logging                                                |

## Configuration Examples

Running Poglink with the default data directory (`~/.poglink`)

```bash
poglink
```

Running Poglink with data stored in `~/bots/poglink/data`

```bash
poglink --data-dir ~/bots/poglink/data
```

Running Poglink with multiple rates urls

```bash
poglink --rates-urls http://arkdedicated.com/dynamicconfig.ini,http://arkdedicated.com/pc_smalltribes_dynamicconfig.ini
```