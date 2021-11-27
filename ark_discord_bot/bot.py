from discord.ext import commands
import yaml
import ark_discord_bot
import argparse
import os
import logging

# https://discord.com/api/oauth2/authorize?client_id=912847784477065278&permissions=117760&scope=bot//
logger = logging.getLogger("ark-discord-bot")


def parse_list(raw):
    return [word.strip() for word in raw.split(",")]


def cli():
    # Configure logging for CLI usage.
    logger.setLevel(level=logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Define CLI arguments.
    parser = argparse.ArgumentParser(
        description="""
        Bot for sending messages to Discord whenever ARK Web API changes.
        
        This bot requires some configuration parameters to be set. They can either
        be provided via a config file, CLI args, or environment variables. These
        values are set using the following order of priority:

            1. CLI Arguments
            2. Configuration file
            3. Environment Variables
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-c",
        "--config-path",
        type=str,
        help="Path to configuration file (YAML). Also can be set via BOT_CONFIG_PATH environment variable.",
    )
    parser.add_argument(
        "-t",
        "--token",
        type=str,
        help="API token for ARK. Also can be set via BOT_TOKEN environment variable.",
    )
    parser.add_argument(
        "-p",
        "--polling-delay",
        type=float,
        default=5,
        help="Polling period in seconds. Also can be set via BOT_POLLING_PERIOD environment variable.",
    )
    parser.add_argument(
        "-a",
        "--allowed-roles",
        type=parse_list,
        help="Comma-separated list of allowed roles. Also can be set via BOT_ALLOWED_ROLES environment variable.",
    )
    parser.add_argument(
        "--rates-url",
        help="URL for ARK rates. Also can be set via BOT_RATES_URL environment variable.",
    )
    parser.add_argument(
        "--rates-channel-id",
        help="Discord 'rates' channel ID. Also can be set via BOT_RATES_CHANNEL_ID environment variable.",
    )
    parser.add_argument(
        "--bans-url",
        help="URL for ARK bans. Also can be set via BOT_BANS_URL environment variable.",
    )
    parser.add_argument(
        "--bans-channel-id",
        help="Discord 'bans' channel ID. Also can be set via BOT_BANS_CHANNEL_ID environment variable.",
    )

    # Load arguments from CLI
    args = parser.parse_args()

    # Attempt to load config values from file if provided
    config_path = args.config_path or os.getenv("BOT_CONFIG_PATH")
    logger.debug(f"CONFIG_PATH: {config_path}")
    if config_path:
        try:
            with open(os.path.expanduser(config_path)) as f:
                config = yaml.safe_load(f)
        except FileNotFoundError as e:
            logger.error(f"Could not find config file at specified location: {config_path}")
            exit(1)
    else:
        config = {}

    # For each configuration value, attempt to obtain value in the following order of priority:
    config["allowed_roles"] = (
        args.allowed_roles
        or config.get("allowed_roles")
        or os.getenv("BOT_ALLOWED_ROLES")
    )
    config["token"] =  config.get("token") or args.token or os.getenv("BOT_TOKEN")
    config["polling_delay"] = (
        args.polling_delay 
        or config.get("polling_delay")
        or os.getenv("BOT_POLLING_DELAY")
    )
    config["rates_url"] = (
        args.rates_url
        or config.get("rates_url")
        or os.getenv("BOT_RATES_URL")
        or "http://arkdedicated.com/dynamicconfig.ini"
    )
    config["rates_channel_id"] = (
        args.rates_channel_id
        or config.get("rates_channel_id")
        or os.getenv("BOT_RATES_CHANNEL_ID")
    )
    config["bans_url"] = (
        args.bans_url
        or config.get("bans_url")
        or os.getenv("BOT_BANS_URL")
        or "http://arkdedicated.com/bansummary.txt"
    )
    config["bans_channel_id"] = (
        args.bans_channel_id
        or config.get("bans_channel_id")
        or os.getenv("BOT_BANS_CHANNEL_ID")
    )

    if not config.get("token"):
        logger.error("No Token specified.")
        exit(1)

    run(config)


def run(config):

    TOKEN = config["token"]
    ALLOWED_ROLES = ["Administrator", "Tech Administrator", "dot"]
    client = commands.Bot(".")

    # load a cog
    @client.command()
    @commands.has_any_role(*ALLOWED_ROLES)
    async def load(ctx, extension):
        client.load_extension(f"ark_discord_bot.cogs.{extension}")

    # unload a cogcd
    @client.command()
    @commands.has_any_role(*ALLOWED_ROLES)
    async def unload(ctx, extension):
        client.unload_extension(f"ark_discord_bot.cogs.{extension}")

    # reload a cog
    @client.command()
    @commands.has_any_role(*ALLOWED_ROLES)
    async def reload(ctx, extension):
        client.unload_extension(f"ark_discord_bot.cogs.{extension}")
        client.load_extension(f"ark_discord_bot.cogs.{extension}")
        await ctx.send(f"Extension '{extension}' reloaded.")

    # load all cogs on boot
    for ext in ark_discord_bot.cogs.__all__:
        client.load_extension(f"ark_discord_bot.cogs.{ext}")

    # run the bot
    client.run(TOKEN)


if __name__ == "__main__":

    cli()