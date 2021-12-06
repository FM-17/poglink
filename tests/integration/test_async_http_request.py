import aiohttp
import requests
import aiohttp
import pytest
from ark_discord_bot.models import RatesStatus


def test_bansummary_request(configured_httpserver, sample_bansummary_txt):
    resp = requests.get(configured_httpserver.url_for("/bansummary.txt"))
    assert resp.text == sample_bansummary_txt


@pytest.mark.asyncio
async def test_async_bansummary_request(configured_httpserver, sample_bansummary_txt):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            configured_httpserver.url_for("/bansummary.txt"),
            headers={"Pragma": "no-cache", "Cache-Control": "no-cache"},
        ) as resp:
            text = await resp.text()
            assert text == sample_bansummary_txt


@pytest.mark.asyncio
async def test_rates_changed(configured_httpserver, sample_dynamicconfig_changed_ini):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            configured_httpserver.url_for("/dynamicconfig.ini"),
            headers={"Pragma": "no-cache", "Cache-Control": "no-cache"},
        ) as resp:
            text = await resp.text()

    rates_diff = RatesStatus.from_raw(text).get_diff(RatesStatus.from_raw(sample_dynamicconfig_changed_ini))
    assert len(rates_diff.items) == 3
    assert set([item.key for item in rates_diff.items]) == set(
        [
            "HarvestAmountMultiplier",
            "MatingIntervalMultiplier",
            "HexagonRewardMultiplier",
        ]
    )
