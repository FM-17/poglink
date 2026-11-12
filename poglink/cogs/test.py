import discord
from discord import app_commands
from discord.ext import commands

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
    @app_commands.command()  # create a command within cog
    @app_commands.checks.has_any_role(*ALLOWED_ROLES)
    async def test(self, interaction: discord.Interaction):

        # generate embed
        embed = discord.Embed(title="Test", color=0x069420)
        embed.description = "Bot online!"

        await interaction.response.send_message(embed=embed)


# add cog to client
async def setup(client):
    await client.add_cog(Test(client))
