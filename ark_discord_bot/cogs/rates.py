import discord
from discord.ext import commands
import asyncio
import aiohttp
import logging
import yaml
import os

# create cog class 
class Rates(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
        self.webpage_url = client.config.rates_url
        self.channel_id = client.config.rates_channel_id
        self.polling_delay = client.config.polling_delay
        self.allowed_roles = client.config.allowed_roles
        self.keyMapping = {
            "TamingSpeedMultiplier":"Taming",
            "HarvestAmountMultiplier":"Harvesting",
            "XPMultiplier":"XP",
            "MatingIntervalMultiplier":"Mating Interval",
            "BabyMatureSpeedMultiplier":"Maturation",
            "EggHatchSpeedMultiplier":"Hatching",
            "BabyCuddleIntervalMultiplier":"Cuddle Interval",
            "BabyImprintAmountMultiplier":"Imprinting",
            "HexagonRewardMultiplier":"Hexagon Reward",
        }
    async def webpage_changed(self,response):
    
        # create content.txt if not created
        if not os.path.exists("local/last_rates.txt"):
            open("local/last_rates.txt", 'w+').close()     

        # read last_rates 
        file = open("local/last_rates.txt", 'r')
        last_rates = file.read() 
        file.close()

        # compare responses, use splitlines to handle carriage returns and newlines
        if (''.join(response.splitlines())) == (''.join(last_rates.splitlines())):
            return False
        else:
            # update response if changed
            file = open("local/last_rates.txt", 'w')
            file.write(response) 
            file.close()
            return True

    async def send_embed(self):
        # read last_rates 
        file = open("local/last_rates.txt", 'r')
        last_rates = file.read() 
        file.close()

        # format response for embed
        response_dict = dict([p.split('=') for p in last_rates.split('\n')])
        response_dict_pretty = {self.keyMapping.get(k, k): (str(v.rstrip('.0')) + "×") for k, v in response_dict.items()}

        # generate embed
        embed=discord.Embed(title="ARK's official server rates have just been updated!", color=0x069420)
        embed.description="\n".join(["**"+ v + "**" + " " + k for k,v in response_dict_pretty.items()])

        # send embed
        channel = self.client.get_channel(self.channel_id)
        await channel.send(embed=embed)

    # Events
    @commands.Cog.listener() 
    async def on_ready(self):
        print("Cog Ready: Rates")   
        log = logging.getLogger(__name__)
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