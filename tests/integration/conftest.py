import pytest

from poglink.bot import ConfigurableBot


@pytest.fixture()
def sample_bot(configured_httpserver):
    bot = ConfigurableBot(
        ".",
        {
            "bans_url": configured_httpserver.url_for("/bansummary.txt"),
            "rates_urls": configured_httpserver.url_for("/dynamicconfig.ini"),
            "data_dir": "tests/data",
        },
    )
    return bot
