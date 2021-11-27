import discord
from discord.ext import commands
import asyncio
import aiohttp
import logging
import yaml
import os

# create cog class 
class Bans(commands.Cog):
    
    def __init__(self, client):
        self.client = client

        self.webpage_url = client.config.bans_url
        self.channel_id = client.config.bans_channel_id
        self.polling_delay = client.config.polling_delay
        self.allowed_roles = client.config.allowed_roles

    async def webpage_changed(self,response):
        # TODO: Move to a hidden user directory (~/.ark-discord-bot/last_bans.txt)
        # create content.txt if not created
        if not os.path.exists("local/last_bans.txt"):
            open("local/last_bans.txt", 'w+').close()     

        # read last_bans 
        file = open("local/last_bans.txt", 'r')
        last_bans = file.read() 
        file.close()

        # compare responses, use splitlines to handle carriage returns and newlines
        if (''.join(response.splitlines())) == (''.join(last_bans.splitlines())):
            return False
        else:
            # update response if changed
            file = open("local/last_bans.txt", 'w')
            file.write(response) 
            file.close()
            return True

    async def send_embed(self):
        # read last_bans 
        file = open("local/last_bans.txt", 'r')
        last_bans = file.read() 
        file.close()

        # generate embed
        embed=discord.Embed(title="ARK Ban Summary", color=0x069420)
        embed.description=last_bans

        # send embed
        channel = self.client.get_channel(self.channel_id)
        await channel.send(embed=embed)

    # Events
    @commands.Cog.listener() 
    async def on_ready(self):
        print("Cog Ready: Bans")   
        # TODO: Move this outside of the class
        log = logging.getLogger(__name__)
        # TODO: Set logging config in outer code; subsequent calls to basicConfig don't actually do anything
        logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(asctime)s %(message)s')
        
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.webpage_url, headers={'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}) as response:
                        response = await response.text()
                        if await self.webpage_changed(response):
                            log.info("Webpage updated.")
                            await self.send_embed()
                        else:
                            log.info("Webpage not updated.")
            except Exception as e:
                log.error(f"Error checking webpage: {e}")
            
            await asyncio.sleep(self.polling_delay)

# add cog to client
def setup(client):
    client.add_cog(Bans(client))


            # "TamingSpeedMultiplier": ":t_rex: Taming",
            # "HarvestAmountMultiplier": ":pick: Harvesting",
            # "XPMultiplier": ":sparkles: XP",
            # "MatingIntervalMultiplier": ":two_hearts: Mating Interval",
            # "BabyMatureSpeedMultiplier": ":hatching_chick: Maturation",
            # "EggHatchSpeedMultiplier": ":egg: Hatching",
            # "BabyCuddleIntervalMultiplier": ":hugging: Cuddle Interval",
            # "BabyImprintAmountMultiplier": ":paw_prints: Imprinting",
            # "HexagonRewardMultiplier": ":gem: Hexagon Reward",