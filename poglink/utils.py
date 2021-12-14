import argparse


def parse_list(raw):
    """Takes a string representation of a comma separated list and returns a list
    of elements with trimmed whitespace.

    Args:
        raw (str): Comma separated list as a string.

    Returns:
        List[str]: List of trimmed strings.
    """
    return [word.strip() for word in raw.split(",")]


def setup_argparse():
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
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-d",
        "--data-dir",
        help="Directory in which to store persistent data and config file. Defaults to ~/.poglink",
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
        help="Polling period in seconds. Also can be set via BOT_POLLING_PERIOD environment variable.",
    )
    parser.add_argument(
        "-a",
        "--allowed-roles",
        type=parse_list,
        help="Comma-separated list of allowed roles. Also can be set via BOT_ALLOWED_ROLES environment variable.",
    )
    parser.add_argument(
        "--rates-urls",
        type=parse_list,
        help="Comma-separated list of URLs for ARK rates. Also can be set via BOT_RATES_URLS environment variable.",
    )
    parser.add_argument(
        "--rates-channel-id",
        help="Discord 'rates' channel ID. Also can be set via BOT_RATES_CHANNEL_ID environment variable.",
    )
    # parser.add_argument(
    #     "--bans-url",
    #     help="URL for ARK bans. Also can be set via BOT_BANS_URL environment variable.",
    # ) # TODO: Reimplement when bans are enabled
    # parser.add_argument(
    #     "--bans-channel-id",
    #     help="Discord 'bans' channel ID. Also can be set via BOT_BANS_CHANNEL_ID environment variable.",
    # ) # TODO: Reimplement when bans are enabled
    parser.add_argument("--debug", action="store_true", help="Set log level to DEBUG.")

    return parser
