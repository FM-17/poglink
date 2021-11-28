import os
import logging
import yaml
from ark_discord_bot.utils import parse_list

logger = logging.getLogger(__name__)


DEFAULT_CONFIG = {
    "allowed_roles": None,
    "polling_delay": 60,
    "rates_url": "http://arkdedicated.com/dynamicconfig.ini",
    "bans_url": "http://arkdedicated.com/bansummary.txt",
    "rates_channel_id": None,
    "bans_channel_id": None,
    "token": None,
    "output_dir": "~/.ark-discord-bot",
}

REQUIRED_VALUES = [
    "token",
    "rates_channel_id",
    "bans_channel_id",
]


def setup_config(args, default_config=DEFAULT_CONFIG):
    # Attempt to load config values from file if provided
    config_path = (
        args.config_path
        or os.getenv("BOT_CONFIG_PATH")
        or "~/.ark-discord-bot/config.yaml"
    )
    if config_path:
        try:
            with open(os.path.expanduser(config_path)) as f:
                config_from_file = yaml.safe_load(f)
        except FileNotFoundError as e:
            logger.error(
                f"Could not find config file at specified location: {config_path}"
            )
            exit(1)
    else:
        config_from_file = {}

    # For each configuration value, attempt to obtain value in the specified order of priority:
    config = {}
    for key, default_val in default_config.items():
        config[key] = (
            getattr(args, key)
            or config_from_file.get(key)
            or os.getenv(f"BOT_{key.upper()}")
            or default_val
        )

    # handle special case for list parsing
    if isinstance(config["allowed_roles"], str):
        try:
            config["allowed_roles"] = parse_list(config["allowed_roles"])
        except TypeError as e:
            logger.warning(
                f"Incorrect variable format; should be comma separated list: {e}"
            )

    return config
