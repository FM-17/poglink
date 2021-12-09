import asyncio
import copy
import json
import logging
import os
from json.decoder import JSONDecodeError
from urllib.parse import urlparse

import aiohttp
import discord
from ark_discord_bot.models import RatesStatus
from discord.ext import commands

logger = logging.getLogger(__name__)

# create cog class
class Rates(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.webpage_urls = client.config.rates_urls
        self.channel_id = client.config.rates_channel_id
        self.polling_delay = client.config.polling_delay
        self.allowed_roles = client.config.allowed_roles
        self.data_dir = os.path.expanduser(client.config.data_dir)
        self.output_paths = [
            os.path.join(
                self.data_dir,
                f"last_{os.path.splitext(os.path.basename(urlparse(url).path))[0]}.json",
            )
            for url in client.config.rates_urls
        ]
        self.keyMapping = {
            "TamingSpeedMultiplier": "Taming",
            "HarvestAmountMultiplier": "Harvesting",
            "XPMultiplier": "XP",
            "MatingIntervalMultiplier": "Mating Interval",
            "BabyMatureSpeedMultiplier": "Maturation",
            "EggHatchSpeedMultiplier": "Hatching",
            "BabyCuddleIntervalMultiplier": "Cuddle Interval",
            "BabyImprintAmountMultiplier": "Imprinting",
            "HexagonRewardMultiplier": "Hexagon Reward",
        }

        # Create parent directory for persistent data if it doesn't exist yet
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    @staticmethod
    async def get_current_rates(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers={"Pragma": "no-cache", "Cache-Control": "no-cache"},
            ) as response:
                response = await response.text()
                rates = RatesStatus.from_raw(response)
                return rates

    async def send_embed(self, description):

        # generate embed
        embed = discord.Embed(
            title="ARK's official server rates have just been updated!", color=0x069420
        )
        embed.description = description

        # send embed
        channel = self.client.get_channel(self.channel_id)
        message = await channel.send(embed=embed)

        # if in announcement channel, publish message
        if message.channel.type == discord.ChannelType.news:
            logger.info("Announcement channel detected: Publishing message")
            await message.publish()

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Cog Ready: Rates")

        while True:
            for url, output_path in zip(self.webpage_urls, self.output_paths):
                # get current rates from ARK Web API
                logger.info(f"Retrieving current rates at {url}")
                try:
                    rates = await self.get_current_rates(url)

                except ValueError:
                    logger.error("Please confirm that rates url(s) are correct")
                except Exception as e:
                     logger.error(f"Could not retrieve rates from ARK Web API: {e}")
                     await asyncio.sleep(self.polling_delay)
                     continue

                # get old rates from file
                try:
                    with open(output_path) as f:
                        last_rates_dict = json.load(f)
                except (FileNotFoundError, JSONDecodeError) as e:
                    logger.warn(f"Problem loading file at {output_path}: {e}")
                    last_rates_dict = copy.deepcopy(rates).to_dict()
                    try:
                        with open(output_path, "w+") as f:
                            json.dump(rates.to_dict(), f, indent=4)
                    except Exception as e:
                        logger.error(e)
                        await asyncio.sleep(self.polling_delay)
                        continue

                last_rates = RatesStatus.from_dict(last_rates_dict)

                # compare rates to last rates
                rates_diff = rates.get_diff(last_rates)

                if rates_diff.items:

                    # save rates to file
                    try:
                        with open(output_path, "w+") as f:
                            json.dump(rates.to_dict(), f, indent=4)
                    except Exception as e:
                        logger.error(e)
                        await asyncio.sleep(self.polling_delay)
                        continue

                    # generate and send embed
                    logger.info(f"Rates at {url} changed - sending embed")
                    embed_description = rates_diff.to_embed(rates)
                    await self.send_embed(embed_description)

            await asyncio.sleep(self.polling_delay)


# add cog to client
def setup(client):
    client.add_cog(Rates(client))
