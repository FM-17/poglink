import logging
import os

import yaml

from poglink.error import ConfigReadError
from poglink.utils import parse_bool, parse_list

logger = logging.getLogger(__name__)

MIN_POLLING_DELAY = 5

DEFAULT_CONFIG = {
    "allowed_roles": [],
    "polling_delay": 60,
    "rates_urls": [
        {
            "server_name": "Official",
            "url": "https://cdn2.arkdedicated.com/asa/dynamicconfig.ini",
            "color": "0x63BCC3",
        }
    ],
    # "bans_url": "http://arkdedicated.com/bansummary.txt",
    "rates_channel_id": None,
    # "bans_channel_id": None, # TODO: Reimplement when bans are enabled
    "token": None,
    "data_dir": "~/.poglink",
    "send_embed_on_startup": False,
}

REQUIRED_VALUES = [
    "token",
    "rates_channel_id",
    # "bans_channel_id", # TODO: Reimplement when bans are enabled
]

LIST_VALUES = [
    "allowed_roles",
]

BOOLEAN_VALUES = ["send_embed_on_startup"]


def setup_config(args, default_config=DEFAULT_CONFIG):
    # Attempt to load config values from file if provided
    data_dir = os.path.expanduser(
        args.data_dir or os.getenv("BOT_DATA_DIR") or DEFAULT_CONFIG.get("data_dir")
    )
    config_path = os.path.join(data_dir, "config.yaml")
    logger.debug(f"Setting up configuration. Checking for config file: {config_path}")

    if os.path.exists(config_path):
        try:
            with open(os.path.expanduser(config_path)) as f:
                config_from_file = yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Problem reading configuration file at {config_path}: {e}")
            raise ConfigReadError(e) from e
    else:
        logger.warning(
            f"No configuration file found at {config_path}. Configuration must be set via CLI args or environment variables."
        )
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

    # handle special cases for boolean values
    for param in BOOLEAN_VALUES:
        if not isinstance(config[param], bool):
            config[param] = parse_bool(config[param])

    # handle special cases for list parsing
    for val in LIST_VALUES:
        if isinstance(config[val], str):
            config[val] = parse_list(config[val])
        elif isinstance(config[val], list):
            pass
        else:
            logger.warning(
                f"Incorrect variable format for {val}; should be comma separated list. Actual value: {config[val]}"
            )

    # handle special case for polling delay
    if config["polling_delay"] < MIN_POLLING_DELAY:
        logger.warning(
            f"Polling delay ({config['polling_delay']}) below minimum value. Setting to minimum value ({MIN_POLLING_DELAY})."
        )
        config["polling_delay"] = MIN_POLLING_DELAY

    logger.debug(f"Configuration loaded from sources: {config}")
    return config
