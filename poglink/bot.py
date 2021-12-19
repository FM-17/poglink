import logging
import os

import yaml
from discord.ext import commands

logger = logging.getLogger(__name__)


class BotConfig:
    def __init__(
        self,
        token=None,
        rates_channel_id=None,
        bans_channel_id=None,
        polling_delay=None,
        allowed_roles=None,
        rates_urls=None,
        # bans_url=None,
        data_dir=None,
        **kwargs,
    ) -> None:
        self.token = token
        self.rates_channel_id = rates_channel_id
        self.bans_channel_id = bans_channel_id
        self.polling_delay = polling_delay
        self.allowed_roles = allowed_roles
        self.rates_urls = rates_urls
        # self.bans_url = bans_url
        self.data_dir = data_dir

        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    @classmethod
    def from_file(cls, config_path):
        """Loads bot configuration from a file. Ideally YAML, but should also work for JSON.

        Args:
            config_path (str): Path to config file (or to directory containing file named 'config.yaml')

        Raises:
            Exception: Problem loading file.
            FileNotFoundError: File does not exist at specified location.

        Returns:
            BotConfig: Object containing bot configuration.
        """
        fullpath = os.path.expanduser(config_path)
        if os.path.isdir(fullpath):
            fullpath = os.path.join(fullpath, "config.yaml")

        logger.debug(f"Loading configuration from file: {config_path}")
        if os.path.isfile(fullpath):
            try:
                with open(fullpath) as f:
                    config_from_file = yaml.safe_load(f)
            except Exception as e:
                logger.error(
                    f"Could not read config file at specified location: {config_path}"
                )
                raise Exception(f"Could not read file at {fullpath}")
        else:
            logger.error(f"File does not exist at location: {fullpath}")
            raise FileNotFoundError("File does not exist at location")

        return cls.from_dict(config_from_file)


class ConfigurableBot(commands.Bot):
    def __init__(self, command_prefix, config_dict, **kwargs):
        self.config = BotConfig.from_dict(config_dict)

        super().__init__(command_prefix, **kwargs)
