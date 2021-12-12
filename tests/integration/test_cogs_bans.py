import pytest
import aiohttp
from poglink.cogs.bans import Bans
from poglink.bot import ConfigurableBot


@pytest.fixture()
def sample_bot(configured_httpserver):
    bot = ConfigurableBot(
        ".",
        {
            "bans_url": configured_httpserver.url_for("/bansummary.txt"),
            "rates_url": configured_httpserver.url_for("/dynamicconfig.ini"),
            "data_dir": "tests/data",
        },
    )
    return bot


@pytest.fixture()
def bans_cog(sample_bot):
    bans_cog = Bans(sample_bot)
    return bans_cog


@pytest.mark.asyncio
async def test_bans_webpage_changed(bans_cog, configured_httpserver, last_bans):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            configured_httpserver.url_for("/bansummary.txt"),
            headers={"Pragma": "no-cache", "Cache-Control": "no-cache"},
        ) as resp:
            text = await resp.text()

    changed_status = await bans_cog.webpage_changed(text)
    assert text == last_bans
    assert changed_status == False

    async with aiohttp.ClientSession() as session:
        async with session.get(
            configured_httpserver.url_for("/bansummary-changed.txt"),
            headers={"Pragma": "no-cache", "Cache-Control": "no-cache"},
        ) as resp:
            text = await resp.text()

    changed_status = await bans_cog.webpage_changed(text)
    assert changed_status == True
