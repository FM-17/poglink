import copy

import pytest

from poglink.bot import BotConfig, ConfigurableBot


@pytest.fixture
def sample_config():
    return {
        "token": "abcd",
        "rates_channel_id": "1234",
        "bans_channel_id": "4321",
        "polling_delay": 69,
        "allowed_roles": ["admin"],
        "rates_urls": ["www.arkrates.com"],
        "data_dir": "/my/fake/dir",
    }


@pytest.fixture
def sample_config_singular(sample_config):
    config = copy.deepcopy(sample_config)
    config.update({"allowed_roles": "regular_user", "rates_urls": "www.google.com"})
    return config


def test_botconfig_from_dict(sample_config):
    botconfig = BotConfig.from_dict(sample_config)

    assert botconfig.token == "abcd"
    assert botconfig.rates_channel_id == "1234"
    assert botconfig.bans_channel_id == "4321"
    assert botconfig.polling_delay == 69
    assert botconfig.allowed_roles == ["admin"]
    assert botconfig.rates_urls == ["www.arkrates.com"]
    assert botconfig.data_dir == "/my/fake/dir"


def test_botconfig_singular_vals(sample_config_singular):
    botconfig = BotConfig.from_dict(sample_config_singular)

    assert botconfig.allowed_roles == ["regular_user"]
    assert botconfig.rates_urls == ["www.google.com"]


def test_botconfig_from_file(
    sample_application_config_yaml, sample_application_config_json
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
    assert botconfig_yaml.rates_urls == ["http://arkdedicated.com/dynamicconfig.ini"]
    assert botconfig_yaml.data_dir == None
