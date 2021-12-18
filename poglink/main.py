import logging
import os

import discord
from discord.ext import commands

import poglink
from poglink.bot import ConfigurableBot
from poglink.config import REQUIRED_VALUES, setup_config
from poglink.utils import setup_argparse

logger = logging.getLogger("poglink")


def cli():
    # Configure logging for CLI usage.
    logging.getLogger().setLevel(level=logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    ch.setFormatter(formatter)
    logging.getLogger().addHandler(ch)

    # Define CLI arguments.
    parser = setup_argparse()

    # Load arguments from CLI
    args = parser.parse_args()

    # Override default log level
    if args.debug or os.getenv("BOT_DEBUG", "").lower() == "true":
        ch.setLevel(logging.DEBUG)
        logger.debug("Debug mode activated.")

    # Set up configuration dict
    config_dict = setup_config(args)

    logger.debug(f"Running with config: {config_dict}")

    # Check for required values
    missing_vals = []
    for val in REQUIRED_VALUES:
        if not config_dict.get(val):
            missing_vals.append(val)
    if len(missing_vals) > 0:
        logger.error(f"Missing required configuration variables: {missing_vals}")
        exit(1)

    run(**config_dict)


def run(**kwargs):
    client = ConfigurableBot(".", kwargs)  # passing as dict, not unpacked kwargs

    # load a cog
    @client.command()
    @commands.has_any_role(*client.config.allowed_roles)
    async def load(ctx, extension):
        logger.debug(f"Loading extension: {extension}")
        client.load_extension(f"poglink.cogs.{extension}")

    # unload a cogcd
    @client.command()
    @commands.has_any_role(*client.config.allowed_roles)
    async def unload(ctx, extension):
        logger.debug(f"Unloading extension: {extension}")
        client.unload_extension(f"poglink.cogs.{extension}")

    # reload a cog
    @client.command()
    @commands.has_any_role(*client.config.allowed_roles)
    async def reload(ctx, extension):
        logger.debug(f"Reloading extension: {extension}")
        client.unload_extension(f"poglink.cogs.{extension}")
        client.load_extension(f"poglink.cogs.{extension}")
        await ctx.send(f"Extension '{extension}' reloaded.")

    # load all cogs on boot
    for ext in poglink.cogs.__all__:
        logger.debug(f"Loading extension: {ext}")
        if ext != "bans":  # TODO: Reimplement when bans are enabled
            client.load_extension(f"poglink.cogs.{ext}")

    # run the bot
    try:
        client.run(client.config.token)
    except discord.errors.LoginFailure as e:
        logger.error("Problem with token.")
        exit(1)


if __name__ == "__main__":

    cli()
