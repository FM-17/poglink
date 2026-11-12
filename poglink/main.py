import logging
import os

import discord
from discord import app_commands

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
    @client.tree.command()
    @app_commands.checks.has_any_role(*client.config.allowed_roles)
    async def load(interaction: discord.Interaction, extension: str):
        logger.debug(f"Loading extension: {extension}")
        await client.load_extension(f"poglink.cogs.{extension}")
        await interaction.response.send_message(f"Extension '{extension}' loaded.")

    # unload a cogcd
    @client.tree.command()
    @app_commands.checks.has_any_role(*client.config.allowed_roles)
    async def unload(interaction: discord.Interaction, extension: str):
        logger.debug(f"Unloading extension: {extension}")
        await client.unload_extension(f"poglink.cogs.{extension}")
        await interaction.response.send_message(f"Extension '{extension}' unloaded.")

    # reload a cog
    @client.tree.command()
    @app_commands.checks.has_any_role(*client.config.allowed_roles)
    async def reload(interaction: discord.Interaction, extension: str):
        logger.debug(f"Reloading extension: {extension}")
        await client.reload_extension(f"poglink.cogs.{extension}")
        await interaction.response.send_message(f"Extension '{extension}' reloaded.")

    # run the bot
    try:
        client.run(client.config.token)
    except discord.errors.LoginFailure as e:
        logger.error(f"Problem with token. {e}")
        exit(1)


if __name__ == "__main__":

    cli()
