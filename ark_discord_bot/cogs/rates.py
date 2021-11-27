import discord
from discord.ext import commands
import asyncio
import aiohttp
import logging
import yaml
import os

logger = logging.getLogger(__name__)

# create cog class
class Rates(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.webpage_url = client.config.rates_url
        self.channel_id = client.config.rates_channel_id
        self.polling_delay = client.config.polling_delay
        self.allowed_roles = client.config.allowed_roles
        self.output_dir = os.path.expanduser(client.config.output_dir)
        self.output_path = os.path.join(self.output_dir, "last_rates.txt")
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
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    async def webpage_changed(self, response):

        # read last_rates
        with open(self.output_path) as f:
            last_rates = f.read()

        # compare responses, use splitlines to handle carriage returns and newlines
        if ("".join(response.splitlines())) == ("".join(last_rates.splitlines())):
            return False
        else:
            # update response if changed
            with open(self.output_path, "w+") as f:
                f.write(response)
            return True

    async def send_embed(self):
        # read last_rates
        with open(self.output_path) as f:
            last_rates = f.read()

        # format response for embed
        response_dict = dict([p.split("=") for p in last_rates.split("\n")])
        response_dict_pretty = {
            self.keyMapping.get(k, k): (str(v.rstrip(".0")) + "×")
            for k, v in response_dict.items()
        }

        # generate embed
        embed = discord.Embed(
            title="ARK's official server rates have just been updated!", color=0x069420
        )
        embed.description = "\n".join(
            ["**" + v + "**" + " " + k for k, v in response_dict_pretty.items()]
        )

        # send embed
        channel = self.client.get_channel(self.channel_id)
        await channel.send(embed=embed)

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Cog Ready: Rates")

        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        self.webpage_url,
                        headers={"Pragma": "no-cache", "Cache-Control": "no-cache"},
                    ) as response:
                        response = await response.text()
                        if await self.webpage_changed(response):
                            logger.info("Webpage updated.")
                            await self.send_embed()
                        else:
                            logger.info("Webpage not updated.")
            except Exception as e:
                logger.error(f"Error checking webpage: {e}")

            await asyncio.sleep(self.polling_delay)


# add cog to client
def setup(client):
    client.add_cog(Rates(client))

    # "TamingSpeedMultiplier": ":t_rex: Taming",
    # "HarvestAmountMultiplier": ":pick: Harvesting",
    # "XPMultiplier": ":sparkles: XP",
    # "MatingIntervalMultiplier": ":two_hearts: Mating Interval",
    # "BabyMatureSpeedMultiplier": ":hatching_chick: Maturation",
    # "EggHatchSpeedMultiplier": ":egg: Hatching",
    # "BabyCuddleIntervalMultiplier": ":hugging: Cuddle Interval",
    # "BabyImprintAmountMultiplier": ":paw_prints: Imprinting",
    # "HexagonRewardMultiplier": ":gem: Hexagon Reward",
