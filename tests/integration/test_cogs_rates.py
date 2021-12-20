import os

import pytest

from poglink.cogs.rates import Rates
from poglink.error import RatesFetchError, RatesProcessError, RatesWriteError
from poglink.models.rates import RatesDiffItem


@pytest.fixture()
def rates_cog(sample_bot):
    rates_cog = Rates(sample_bot)
    yield rates_cog

    # Clean up
    for f in rates_cog.output_paths:
        try:
            os.remove(f)
        except:
            pass


@pytest.mark.asyncio
async def test_rates_compare_posted_rates(rates_cog, rates_url_1, rates_url_2):
    output_path = rates_cog.output_paths[0]

    # First request; no changes expected
    rates_diff = await rates_cog.compare_posted_rates(rates_url_1, output_path)
    assert len(rates_diff.items) == 0

    # 2nd request; changes should be returned
    rates_diff = await rates_cog.compare_posted_rates(rates_url_2, output_path)

    assert len(rates_diff.items) == 3
    assert (
        RatesDiffItem(key="HarvestAmountMultiplier", old_val="3.0", new_val="2.0")
        in rates_diff.items
    )
    assert (
        RatesDiffItem(key="MatingIntervalMultiplier", old_val="0.6", new_val="0.7")
        in rates_diff.items
    )
    assert (
        RatesDiffItem(key="HexagonRewardMultiplier", old_val="1.5", new_val="2.5")
        in rates_diff.items
    )


@pytest.mark.asyncio
async def test_rates_compare_posted_rates_bad_fetch(rates_cog):
    output_path = rates_cog.output_paths[0]

    with pytest.raises(RatesFetchError):
        rates_diff = await rates_cog.compare_posted_rates(
            "http://localhost:5000/bogus-url.txt", output_path
        )


@pytest.mark.asyncio
async def test_rates_compare_posted_rates_bad_parse(rates_cog):
    output_path = rates_cog.output_paths[0]

    with pytest.raises(RatesProcessError):
        rates_diff = await rates_cog.compare_posted_rates(
            "https://www.google.com", output_path
        )


@pytest.mark.asyncio
async def test_rates_compare_posted_rates_bad_write(rates_cog, rates_url_1):

    with pytest.raises(RatesWriteError):
        rates_diff = await rates_cog.compare_posted_rates(
            rates_url_1, "/invalid/directory"
        )
