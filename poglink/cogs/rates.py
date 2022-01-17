import asyncio
import logging
import os
import re
import time
from urllib.parse import urlparse

import aiohttp
import discord
from discord.ext import commands

from poglink.config import MIN_POLLING_DELAY
from poglink.error import RatesFetchError, RatesProcessError
from poglink.models import RatesStatus

logger = logging.getLogger(__name__)

EMBED_IMAGE = "https://i.stack.imgur.com/Fzh0w.png"

# create cog class
class Rates(commands.Cog):
    DEFAULT_SERVER_INFO = {
        "smalltribes": {
            "short_name": "Smalltribes",
            "color": 0xA34C44,
        },
        "arkpocalypse": {
            "short_name": "Arkpocalypse",
            "color": 0xF8DE74,
        },
        "conquest": {
            "short_name": "Conquest/Classic",
            "color": 0x6DFF90,
        },
        None: {
            "short_name": "Official",
            "color": 0x63BCC3,
        },
    }

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
        self.last_rates = [None for _ in self.webpage_urls]
        self.stable_rates = [None for _ in self.webpage_urls]
        self.consecutive_count = [0 for _ in self.webpage_urls]
        logger.debug(f"URLs: {self.webpage_urls}, Output paths: {self.output_paths}")
        # Create parent directory for persistent data if it doesn't exist yet
        if not os.path.exists(self.data_dir):
            logger.info(f"Data directory doesn't exist yet; creating: {self.data_dir}")
            os.makedirs(self.data_dir)

    @staticmethod
    async def get_current_rates(url):
        logger.debug(f"Requesting current server rates")
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    url,
                    headers={"Pragma": "no-cache", "Cache-Control": "no-cache"},
                ) as response:
                    response = await response.text()
                    rates = RatesStatus.from_raw(response)
                    logger.debug(f"Obtained server rates: {RatesStatus}")
                    return rates
            except ValueError as e:
                raise RatesProcessError(e) from e
            except Exception as e:
                raise RatesFetchError(e) from e

    async def send_embed(self, description, url):
        # generate embed
        logger.debug(f"Attempting to send embed. desc: {description}, url: {url}")
        try:
            match = re.match(
                "(?P<host>.*\/)?(?:(?P<platform>.*)\_(?P<game_mode>.*)\_)?dynamicconfig\.ini",
                os.path.basename(urlparse(url).path),
            )
            if match:
                server_match_dict = match.groupdict()
            else:
                server_match_dict = {}

            server_meta = self.DEFAULT_SERVER_INFO.get(
                server_match_dict.get("game_mode")
            )
            logger.debug(f"Server meta: {server_meta}")
            # TODO: Add ability to accept custom rates URL

        except Exception as e:
            logger.error(f"Rates url could not be processed: {url} {e}")
            return

        server_name = server_meta.get("short_name")

        embed = discord.Embed(
            description=description,
            title=f"ARK's {server_name} server rates have just been updated!",
            color=server_meta.get("color"),
        )
        embed.set_image(url=EMBED_IMAGE)

        # send embed
        channel = self.client.get_channel(self.channel_id)
        message = await channel.send(embed=embed)

        # if in announcement channel, publish message
        if message.channel.type == discord.ChannelType.news:
            logger.info("Announcement channel detected: Publishing message")
            await message.publish()

    async def compare_and_notify_all(self):
        for idx in range(len(self.webpage_urls)):
            url = self.webpage_urls[idx]

            # Fetch current rates from online
            try:
                current_rates = await self.get_current_rates(url)
            except RatesFetchError as e:
                logger.error(f"Could not retrieve rates from ARK Web API at {url}: {e}")
                continue
            except RatesProcessError as e:
                logger.error(f"Could not process rates URL {url}: {e}")
                continue
            except Exception as e:
                logger.error(e)
                continue

            # Only if last rates exist, get diff
            if self.last_rates[idx]:
                rates_diff = self.last_rates[idx].get_diff(current_rates)

                # If there is a difference, reset consecutive count; otherwise increment it
                if rates_diff.items:
                    self.consecutive_count[idx] = 1
                    self.last_rates[idx] = current_rates
                    logger.info(
                        f"Rates for {url} changed. Resetting consecutive rates count to 1"
                    )
                else:
                    self.consecutive_count[idx] += 1
                    logger.info(
                        f"Rates for {url} unchanged. Consecutive count = {self.consecutive_count[idx]}"
                    )

                if self.consecutive_count[idx] == 2:
                    logger.info(
                        f"New rates have become stable. Comparing against previous stable rates."
                    )
                    if self.stable_rates[idx]:
                        stable_diff = self.stable_rates[idx].get_diff(current_rates)
                        if stable_diff.items:
                            # generate and send embed
                            logger.info(
                                f"Rates at {url} changed since last stable value - sending embed"
                            )
                            embed_description = stable_diff.to_embed()
                            await self.send_embed(embed_description, url)
                    else:
                        logger.info(
                            "No previous stable rates recorded. Updating new stable value, but no updates to publish."
                        )

                    self.stable_rates[idx] = current_rates
            else:
                self.consecutive_count[idx] = 1
                logger.info(f"No previous rates stored yet; skipping.")

            # Update last rates value for next iteration
            self.last_rates[idx] = current_rates

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Cog Ready: Rates")

        while True:
            await self.compare_and_notify_all()
            await asyncio.sleep(self.polling_delay)


# add cog to client
def setup(client):
    client.add_cog(Rates(client))
