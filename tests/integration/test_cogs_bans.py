import aiohttp
import pytest

from poglink.cogs.bans import Bans


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
            assert resp.status == 200
            text = await resp.text()

    changed_status = await bans_cog.webpage_changed(text)
    assert text == last_bans
    assert changed_status == False

    async with aiohttp.ClientSession() as session:
        async with session.get(
            configured_httpserver.url_for("/bansummary-changed.txt"),
            headers={"Pragma": "no-cache", "Cache-Control": "no-cache"},
        ) as resp:
            assert resp.status == 200
            text = await resp.text()

    assert "PC Bans: 42069" in text

    changed_status = await bans_cog.webpage_changed(text)
    assert changed_status == True
