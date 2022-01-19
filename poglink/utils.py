import argparse
import os


def parse_list(raw):
    """Takes a string representation of a comma separated list and returns a list
    of elements with trimmed whitespace.

    Args:
        raw (str): Comma separated list as a string.

    Returns:
        List[str]: List of trimmed strings.
    """
    return [word.strip() for word in raw.split(",")]


def parse_bool(raw):
    """Takes a string representation of a truthy string value and converts it to bool.

    Valid boolean representations include:
        - y/yes/Yes/YES
        - true/True/TRUE
        - 1

    Args:
        raw (str): Truthy value to convert.

    Returns:
        bool: Boolean representation of value.
    """
    if isinstance(raw, str):
        raw = raw.lower()

    return raw in ["y", "yes", "true", "1", 1]


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
    parser.add_argument(
        "--publish-on-startup",
        action="store_true",
        help="Publish current rates found after starting the bot for the first time.",
    )

    return parser


def rotate_backups(full_path, max_copies=2):
    """Rotates backup files by appending sequential integer extensions.

    Example: If ``full_path`` is ``/my/path/to/file.txt``, then calling this function will
    rename / back up the file to ``/my/path/to/file.txt.1``. If another file is then written as
    ``file.txt`` and this function is called again, it will rename the previous backup to
    ``/my/path/to/file.txt.2``, and rename the new file to ``/my/path/to/file.txt.1``.

    The ``max_copies`` parameter controls to what limit this rolling backup is performed. Files
    in excess of this limit are deleted, in a first-in-first-out manner. The ``max_copies`` parameter
    considers the main file in addition to its backups. That is, if ``max_copies`` is set to 3, there
    will never be more than:

    - /my/path/to/file.txt
    - /my/path/to/file.txt.1
    - /my/path/to/file.txt.2

    Args:
        full_path (str): Full path to base file being rotated
        max_copies (int, optional): Maximum number of files to keep (backups + main). Defaults to 2.
    """
    full_path = os.path.expanduser(full_path)

    for i in reversed(range(max_copies)):
        if i == 0:
            old_filename = full_path
        else:
            old_filename = f"{full_path}.{i}"
        new_filename = f"{full_path}.{i+1}"

        if os.path.isfile(old_filename):
            if i == max_copies - 1:
                os.remove(old_filename)
                continue

            os.rename(old_filename, new_filename)
