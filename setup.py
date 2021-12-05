# TODO: Transition to setup.cfg https://setuptools.pypa.io/en/latest/userguide/quickstart.html#transitioning-from-setup-py-to-setup-cfg
from setuptools import find_packages, setup

setup(
    name="ark-discord-bot",
    version="0.0.1",
    description="A bot for notifying of changes to the ARK Web API via Discord.",
    author="FM-17",
    packages=find_packages(),
    install_requires=["discord>=1.7", "pyyaml", "python-dateutil", "jinja2"],
    entry_points={
        "console_scripts": [
            "ark-discord-bot=ark_discord_bot.main:cli",
        ]
    },
)
