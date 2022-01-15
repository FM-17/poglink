import asyncio
import copy
import json
import logging
import os
import re
import time
from json.decoder import JSONDecodeError
from urllib.parse import urlparse

import aiohttp
import discord
from discord.ext import commands

from poglink.config import MIN_POLLING_DELAY
from poglink.error import RatesFetchError, RatesProcessError, RatesWriteError
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
        logger.debug(f"URLs: {self.webpage_urls}, Output paths: {self.output_paths}")
        # Create parent directory for persistent data if it doesn't exist yet
        if not os.path.exists(self.data_dir):
            logger.info(f"Data directory doesn't exist yet; creating: {self.data_dir}")
            os.makedirs(self.data_dir)

    @staticmethod
    async def get_current_rates(url):
        logger.debug(f"Requesting current server rates")
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers={"Pragma": "no-cache", "Cache-Control": "no-cache"},
            ) as response:
                response = await response.text()
                rates = RatesStatus.from_raw(response)
                logger.debug(f"Obtained server rates: {RatesStatus}")
                return rates

    async def send_embed(self, description, url):
        # generate embed
        logger.debug(f"Attempting to send embed. desc: {description}, url: {url}")
        try:
            server_match_dict = (
                re.match(
                    "(?P<host>.*\/)?(?:(?P<platform>.*)\_(?P<game_mode>.*)\_)?dynamicconfig\.ini",
                    os.path.basename(urlparse(url).path),
                )
            ).groupdict()
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

    async def compare_posted_rates(self, webpage_url, output_path):
        # get current rates from ARK Web API
        logger.info(f"Retrieving current rates at {webpage_url}")
        try:
            rates = await self.get_current_rates(webpage_url)
        except ValueError as e:
            raise RatesProcessError(e) from e
        except Exception as e:
            raise RatesFetchError(e) from e

        # get old rates from file
        try:
            with open(output_path) as f:
                last_rates_dict = json.load(f)
        except (FileNotFoundError, JSONDecodeError) as e:
            logger.warning(f"Problem loading file at {output_path}: {e}")
            last_rates_dict = copy.deepcopy(rates).to_dict()
            try:
                with open(output_path, "w+") as f:
                    json.dump(rates.to_dict(), f, indent=4)
            except Exception as e:
                raise RatesWriteError(e) from e

        last_rates = RatesStatus.from_dict(last_rates_dict)

        # compare rates to last rates
        rates_diff = last_rates.get_diff(rates)

        if rates_diff.items:
            # save rates to file
            try:
                with open(output_path, "w+") as f:
                    json.dump(rates.to_dict(), f, indent=4)
            except Exception as e:
                raise RatesWriteError(e) from e

        return rates_diff

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Cog Ready: Rates")

        while True:
            for url, output_path in zip(self.webpage_urls, self.output_paths):
                try:
                    rates_diff = await self.compare_posted_rates(url, output_path)
                except RatesFetchError as e:
                    logger.error(
                        f"Could not retrieve rates from ARK Web API at {url}: {e}"
                    )
                except RatesProcessError as e:
                    logger.error(f"Could not process rates URL {url}: {e}")
                except RatesWriteError as e:
                    logger.error(f"Failed to write rates to {output_path}: {e}")
                except Exception as e:
                    logger.error(e)

                if rates_diff.items:
                    # generate and send embed
                    logger.info(f"Rates at {url} changed - sending embed")
                    embed_description = rates_diff.to_embed()
                    await self.send_embed(embed_description, url)
                else:
                    logger.debug(f"No change in rates at {url}.")

                await asyncio.sleep(self.polling_delay)


# add cog to client
def setup(client):
    client.add_cog(Rates(client))
