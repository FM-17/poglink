import discord
from discord.ext import commands
from discord.utils import get
import os

# https://discord.com/api/oauth2/authorize?client_id=912847784477065278&permissions=117760&scope=bot//

TOKEN = open("local/token.txt", "r").readline()
ALLOWED_ROLES = ['Administrator', 'Tech Administrator', 'dot']
client = commands.Bot(".")

# load a cog
@client.command()
@commands.has_any_role(*ALLOWED_ROLES)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

# unload a cogcd 
@client.command()
@commands.has_any_role(*ALLOWED_ROLES)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

# reload a cog
@client.command()
@commands.has_any_role(*ALLOWED_ROLES)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"Extension '{extension}' reloaded.")

# load all cogs on boot
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}') 

# run the bot
client.run(TOKEN)