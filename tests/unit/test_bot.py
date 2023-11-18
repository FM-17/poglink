import copy
import os

import pytest

from poglink.bot import BotConfig, ConfigurableBot
from poglink.error import ConfigReadError


@pytest.fixture
def sample_config_dict():
    return {
        "token": "abcd",
        "rates_channel_id": "1234",
        "bans_channel_id": "4321",
        "polling_delay": 69,
        "allowed_roles": ["admin"],
        "rates_urls": ["www.arkrates.com"],
        "data_dir": "/my/fake/dir",
        "send_embed_on_startup": True,
    }


@pytest.fixture
def sample_config_dict_singular(sample_config_dict):
    config = copy.deepcopy(sample_config_dict)
    config.update(
        {"allowed_roles": "regular_user", "rates_urls": {"url": "www.google.com"}}
    )
    return config


def test_botconfig_from_dict(sample_config_dict):
    botconfig = BotConfig.from_dict(sample_config_dict)

    assert botconfig.token == "abcd"
    assert botconfig.rates_channel_id == "1234"
    assert botconfig.bans_channel_id == "4321"
    assert botconfig.polling_delay == 69
    assert botconfig.allowed_roles == ["admin"]
    assert botconfig.rates_urls == ["www.arkrates.com"]
    assert botconfig.data_dir == "/my/fake/dir"


def test_botconfig_singular_vals(sample_config_dict_singular):
    botconfig = BotConfig.from_dict(sample_config_dict_singular)

    assert botconfig.allowed_roles == ["regular_user"]
    assert botconfig.rates_urls == {"url": "www.google.com"}


def test_botconfig_from_file(
    sample_application_config_yaml, sample_application_config_json, config_yaml
):
    botconfig_yaml = BotConfig.from_file(sample_application_config_yaml)
    botconfig_json = BotConfig.from_file(sample_application_config_json)

    # YAML and JSON formats both equivalent
    assert botconfig_yaml == botconfig_json

    # Expected values are present
    assert botconfig_yaml.token == "abcd"
    assert botconfig_yaml.rates_channel_id == "1234"
    assert botconfig_yaml.polling_delay == 60
    assert botconfig_yaml.allowed_roles == ["admin", "regular_users"]
    assert botconfig_yaml.rates_urls == [
        {"url": "http://arkdedicated.com/dynamicconfig.ini"}
    ]
    assert botconfig_yaml.data_dir is None
    assert botconfig_yaml.send_embed_on_startup is True

    # Raises error when file doesn't exist
    with pytest.raises(FileNotFoundError):
        BotConfig.from_file("/nonsense/path")

    # Grabs file called config.yaml if provided path is a directory
    botconfig = BotConfig.from_file(os.path.dirname(config_yaml))
    assert botconfig == botconfig_yaml


def test_configurable_bot(sample_config_dict):
    bot = ConfigurableBot(command_prefix=".test", config_dict=sample_config_dict)

    assert bot.config.token == "abcd"
    assert bot.config.rates_channel_id == "1234"
    assert bot.config.bans_channel_id == "4321"
    assert bot.config.polling_delay == 69
    assert bot.config.allowed_roles == ["admin"]
    assert bot.config.rates_urls == ["www.arkrates.com"]
    assert bot.config.data_dir == "/my/fake/dir"
    assert bot.config.send_embed_on_startup is True


def test_comma_separation(sample_application_config_comma_yaml):
    botconfig = BotConfig.from_file(sample_application_config_comma_yaml)

    assert botconfig.allowed_roles == ["admin", "regular_users"]
    assert botconfig.rates_urls == [
        {"url": "http://arkdedicated.com/dynamicconfig.ini"},
        {"url": "http://www.google.com"},
    ]


def test_config_read_error(application_config_broken):
    with pytest.raises(ConfigReadError):
        BotConfig.from_file(application_config_broken)
