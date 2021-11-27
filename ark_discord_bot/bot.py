from discord.ext import commands
import os
import yaml

import ark_discord_bot

# https://discord.com/api/oauth2/authorize?client_id=912847784477065278&permissions=117760&scope=bot//

def main():
    with open('config.yaml') as stream:
        config = yaml.safe_load(stream)

    TOKEN = config['token']
    ALLOWED_ROLES = ['Administrator', 'Tech Administrator', 'dot']
    client = commands.Bot(".")

    # load a cog
    @client.command()
    @commands.has_any_role(*ALLOWED_ROLES)
    async def load(ctx, extension):
        client.load_extension(f'ark_discord_bot.cogs.{extension}')

    # unload a cogcd 
    @client.command()
    @commands.has_any_role(*ALLOWED_ROLES)
    async def unload(ctx, extension):
        client.unload_extension(f'ark_discord_bot.cogs.{extension}')

    # reload a cog
    @client.command()
    @commands.has_any_role(*ALLOWED_ROLES)
    async def reload(ctx, extension):
        client.unload_extension(f'ark_discord_bot.cogs.{extension}')
        client.load_extension(f'ark_discord_bot.cogs.{extension}')
        await ctx.send(f"Extension '{extension}' reloaded.")

    # load all cogs on boot
    for ext in ark_discord_bot.cogs.__all__:
            client.load_extension(f'ark_discord_bot.cogs.{ext}') 

    # run the bot
    client.run(TOKEN)

if __name__ == "__main__":
    main()