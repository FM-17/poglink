import argparse
import logging
import os
import tempfile

import pytest
import yaml

from poglink.config import DEFAULT_CONFIG, setup_config


@pytest.fixture
def cli_config_vals():
    vals = {k: None for k in DEFAULT_CONFIG.keys()}
    vals.update(
        {
            "bans_channel_id": "54321",
            "rates_channel_id": "2468",
            "polling_delay": 2,
        }
    )
    return vals


@pytest.fixture
def args(cli_config_vals):
    return argparse.Namespace(**cli_config_vals)


@pytest.fixture
def file_config_vals():
    return {
        "token": "abcdef",
        "rates_channel_id": "12345",
        "allowed_roles": ["test", "admin"],
    }


@pytest.fixture
def config_dir(file_config_vals):
    with tempfile.TemporaryDirectory() as dirname:
        fullpath = os.path.join(dirname, "config.yaml")
        with open(fullpath, "w+") as f:
            yaml.safe_dump(file_config_vals, f)

        yield dirname


@pytest.fixture
def env(config_dir):
    os.environ["BOT_DATA_DIR"] = config_dir
    os.environ["BOT_RATES_URLS"] = "https://www.google.com,https://www.bing.com"
    os.environ["BOT_TOKEN"] = "fedcba"
    os.environ["BOT_PUBLISH_ON_STARTUP"] = "1"


def test_setup_config(args, env, caplog):
    config = setup_config(args)

    # Values are read from CLI
    assert (
        config.get("bans_channel_id") == None
    )  # "54321", # TODO: Reimplement when bans are enabled

    # Values are read from environment vars
    assert config.get("rates_urls") == [
        "https://www.google.com",
        "https://www.bing.com",
    ]

    # Values are read from File
    assert config.get("allowed_roles") == ["test", "admin"]

    # Default value is populated
    assert (
        config.get("bans_url") == None
    )  # "http://arkdedicated.com/bansummary.txt", # TODO: Reimplement when bans are enabled

    # File takes precedence over env
    assert config.get("token") == "abcdef"

    # CLI takes precedence over file
    assert config.get("rates_channel_id") == "2468"

    # Min polling delay is enforced and logged
    assert config.get("polling_delay") == 5
    with caplog.at_level(logging.WARNING):
        assert "below minimum value" in caplog.text

    # boolean values are interpreted from env var
    assert config.get("publish_on_startup") == True
