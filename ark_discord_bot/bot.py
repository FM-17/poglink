from discord.ext import commands
import os
import yaml
import logging
import json

logger = logging.getLogger(__name__)


class BotConfig:
    def __init__(
        self,
        token=None,
        rates_channel_id=None,
        bans_channel_id=None,
        polling_delay=None,
        allowed_roles=None,
        rates_url=None,
        bans_url=None,
        data_dir=None,
        **kwargs,
    ) -> None:
        self.token = token
        self.rates_channel_id = rates_channel_id
        self.bans_channel_id = bans_channel_id
        self.polling_delay = polling_delay
        self.allowed_roles = allowed_roles
        self.rates_url = rates_url
        self.bans_url = bans_url
        self.data_dir = data_dir

        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    @classmethod
    def from_yaml(cls, config_path):
        fullpath = os.path.expanduser(config_path)
        if os.path.isdir(fullpath):
            fullpath = os.path.join(fullpath, "config.yaml")

        if os.path.isfile(fullpath)    
        try:
            with open() as f:
                config_from_file = yaml.safe_load(f)
        except FileNotFoundError as e:
            logger.error(
                f"Could not find config file at specified location: {config_path}"
            )
            raise e

        return cls.from_dict(config_from_file)

    @classmethod
    def from_json(cls, config_path):
        try:
            with open(os.path.expanduser(config_path)) as f:
                config_from_file = json.load(f)
        except FileNotFoundError as e:
            logger.error(
                f"Could not find config file at specified location: {config_path}"
            )
            raise e

        return cls.from_dict(config_from_file)


class ConfigurableBot(commands.Bot):
    def __init__(self, command_prefix, config_dict, **kwargs):
        self.config = BotConfig.from_dict(config_dict)

        super().__init__(command_prefix, **kwargs)
