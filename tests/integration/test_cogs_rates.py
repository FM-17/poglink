import os

import discord
import discord.ext.test as dpytest
import pytest

from poglink.cogs.rates import EMBED_IMAGE, Rates
from poglink.error import RatesFetchError, RatesProcessError
from poglink.models.rates import RatesDiffItem

SAMPLE_DYNAMICCONFIG_PATH_1 = "tests/data/dynamicconfig-1.ini"
SAMPLE_DYNAMICCONFIG_PATH_2 = "tests/data/dynamicconfig-2.ini"

with open(SAMPLE_DYNAMICCONFIG_PATH_1) as f:
    SAMPLE_DYNAMICCONFIG_1 = f.read()

with open(SAMPLE_DYNAMICCONFIG_PATH_2) as f:
    SAMPLE_DYNAMICCONFIG_2 = f.read()


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
async def test_send_embed(rates_cog):
    # Define an embed that matches what should be published by the cog
    sample_embed = discord.Embed(
        description="test",
        title="ARK's Official server rates have just been updated!",
        color=0x63BCC3,
    )
    sample_embed.set_image(url=EMBED_IMAGE)

    # Publish the embed using the Rates cog
    await rates_cog.send_embed(
        description="test", url="www.mysite.com/dynamicconfig.ini"
    )

    # Ensure embed appears in the queue and nothing else.
    assert dpytest.verify().message().embed(embed=sample_embed)
    assert dpytest.verify().message().nothing()


@pytest.mark.parametrize(
    "sequential_handler",
    [
        (
            SAMPLE_DYNAMICCONFIG_1,
            SAMPLE_DYNAMICCONFIG_1,
            SAMPLE_DYNAMICCONFIG_1,
            SAMPLE_DYNAMICCONFIG_2,
            SAMPLE_DYNAMICCONFIG_2,
        )
    ],
    indirect=True,
)
@pytest.mark.asyncio
async def test_compare_and_notify_all(rates_cog):
    sample_embed = discord.Embed(
        description="3 × Taming\n**2** × Harvesting\n3 × XP\n**0.7** × Mating Interval\n3 × Maturation\n3 × Hatching\n0.6 × Cuddle Interval\n3 × Imprinting\n**2.5** × Hexagon Reward",
        title="ARK's Official server rates have just been updated!",
        color=0x63BCC3,
    )
    sample_embed.set_image(url=EMBED_IMAGE)

    # First request; no diff. First time seeing rates
    await rates_cog.compare_and_notify_all()
    assert dpytest.verify().message().nothing()

    # 2nd request; no diff. Rates are now stable since they've been observed 2 times in a row
    await rates_cog.compare_and_notify_all()
    assert dpytest.verify().message().nothing()

    # 3rd request; still no diff. No change to stable rates
    await rates_cog.compare_and_notify_all()
    assert dpytest.verify().message().nothing()

    # 4th request; new rates found, but not yet stable
    await rates_cog.compare_and_notify_all()
    assert dpytest.verify().message().nothing()

    # 5th request; no diff from previous, which means new rates are stable. Different from previous stable rates, so embed is published
    await rates_cog.compare_and_notify_all()
    assert dpytest.verify().message().embed(embed=sample_embed)

    # Only one embed was published; queue is empty after consuming message above
    assert dpytest.verify().message().nothing()


@pytest.mark.parametrize(
    "sequential_handler",
    [
        (
            SAMPLE_DYNAMICCONFIG_2,
            SAMPLE_DYNAMICCONFIG_2,
            SAMPLE_DYNAMICCONFIG_1,
            SAMPLE_DYNAMICCONFIG_1,
        )
    ],
    indirect=True,
)
@pytest.mark.asyncio
async def test_compare_and_notify_all_reverse(rates_cog):
    sample_embed = discord.Embed(
        description="3 × Taming\n**3** × Harvesting\n3 × XP\n**0.6** × Mating Interval\n3 × Maturation\n3 × Hatching\n0.6 × Cuddle Interval\n3 × Imprinting\n**1.5** × Hexagon Reward",
        title="ARK's Official server rates have just been updated!",
        color=0x63BCC3,
    )
    sample_embed.set_image(url=EMBED_IMAGE)

    # First request; no diff. First time seeing rates
    await rates_cog.compare_and_notify_all()
    assert dpytest.verify().message().nothing()

    # 2nd request; no diff. Rates are now stable since they've been observed 2 times in a row
    await rates_cog.compare_and_notify_all()
    assert dpytest.verify().message().nothing()

    # 3rd request; still no diff. No change to stable rates
    await rates_cog.compare_and_notify_all()
    assert dpytest.verify().message().nothing()

    # 4th request; no diff from previous, which means new rates are stable. Different from previous stable rates, so embed is published
    await rates_cog.compare_and_notify_all()
    print(rates_cog.last_rates[0].to_dict())
    assert dpytest.verify().message().embed(embed=sample_embed)

    # Only one embed was published; queue is empty after consuming message above
    assert dpytest.verify().message().nothing()


@pytest.mark.asyncio
async def test_rates_get_current_rates_bad_fetch(rates_cog):
    output_path = rates_cog.output_paths[0]

    with pytest.raises(RatesFetchError):
        rates_diff = await rates_cog.get_current_rates(
            "http://localhost:5000/bogus-url.txt"
        )


@pytest.mark.asyncio
async def test_rates_get_current_rates_bad_parse(rates_cog):
    output_path = rates_cog.output_paths[0]

    with pytest.raises(RatesProcessError):
        rates_diff = await rates_cog.get_current_rates("https://www.google.com")
