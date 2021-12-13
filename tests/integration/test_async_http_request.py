import aiohttp
import pytest

from poglink.models import RatesStatus


@pytest.mark.asyncio
async def test_async_bansummary_request(configured_httpserver, sample_bansummary_1):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            configured_httpserver.url_for("/bansummary.txt"),
            headers={"Pragma": "no-cache", "Cache-Control": "no-cache"},
        ) as resp:
            text = await resp.text()
            assert text == sample_bansummary_1


@pytest.mark.asyncio
async def test_rates_changed(configured_httpserver, sample_dynamicconfig_2):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            configured_httpserver.url_for("/dynamicconfig.ini"),
            headers={"Pragma": "no-cache", "Cache-Control": "no-cache"},
        ) as resp:
            text = await resp.text()

    rates_diff = RatesStatus.from_raw(text).get_diff(
        RatesStatus.from_raw(sample_dynamicconfig_2)
    )
    assert len(rates_diff.items) == 3
    assert set([item.key for item in rates_diff.items]) == set(
        [
            "HarvestAmountMultiplier",
            "MatingIntervalMultiplier",
            "HexagonRewardMultiplier",
        ]
    )
