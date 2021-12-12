import discord
from discord.ext import commands
from discord.message import MessageType

ALLOWED_ROLES = ["Administrator", "Tech Administrator", "dot"]

# create cog class
class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog Ready: Test")

    # Commands
    @commands.has_any_role(*ALLOWED_ROLES)
    @commands.command()  # create a command within cog
    async def test(self, ctx):

        # generate embed
        embed = discord.Embed(title="Test", color=0x069420)
        embed.description = "Bot online!"

        await ctx.send(embed=embed)


# add cog to client
def setup(client):
    client.add_cog(Test(client))
