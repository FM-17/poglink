from setuptools import find_packages, setup

setup(
    name="ark-discord-bot",
    description="A bot for notifying of changes to the ARK Web API via Discord.",
    author="FM-17",
    packages=find_packages(),
    install_requires=[
        "discord>=1.7",
        "pyyaml"
    ],
    entry_points={
        "console_scripts": [ 
            "ark-discord-bot=ark_discord_bot.bot:cli"
        ]
    }
)