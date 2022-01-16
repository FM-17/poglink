import discord.ext.test
import pytest

from poglink.bot import ConfigurableBot


@pytest.fixture()
def sample_bot(bans_url_1, rates_url_1, event_loop):
    # Define intents required to publish embeds
    intents = discord.Intents.default()
    intents.members = True

    bot = ConfigurableBot(
        ".",
        {
            "bans_url": bans_url_1,
            "rates_urls": [rates_url_1],
            "data_dir": "tests/data",
        },
        loop=event_loop,  # Ensure pytest uses same event loop for async functions as bot
        intents=intents,
    )

    # Configure bot for testing
    discord.ext.test.configure(bot)

    # Override rates channel id with test channel id
    bot.config.rates_channel_id = bot.guilds[0].text_channels[0].id

    return bot


@pytest.fixture
def configured_httpserver(
    httpserver,
    sample_bansummary_1,
    sample_bansummary_2,
    sample_dynamicconfig_1,
    sample_dynamicconfig_2,
):
    httpserver.expect_request("/bansummary.txt").respond_with_data(
        sample_bansummary_1, content_type="text/plain"
    )
    httpserver.expect_request("/bansummary-changed.txt").respond_with_data(
        sample_bansummary_2, content_type="text/plain"
    )
    httpserver.expect_request("/dynamicconfig.ini").respond_with_data(
        sample_dynamicconfig_1, content_type="text/plain"
    )
    httpserver.expect_request("/dynamicconfig-changed.ini").respond_with_data(
        sample_dynamicconfig_2, content_type="text/plain"
    )

    return httpserver


@pytest.fixture
def rates_url_1(configured_httpserver):
    return configured_httpserver.url_for("/dynamicconfig.ini")


@pytest.fixture
def rates_url_2(configured_httpserver):
    return configured_httpserver.url_for("/dynamicconfig-changed.ini")


@pytest.fixture
def bans_url_1(configured_httpserver):
    return configured_httpserver.url_for("/bansummary.text")


@pytest.fixture
def bans_url_2(configured_httpserver):
    return configured_httpserver.url_for("/bansummary-changed.text")
