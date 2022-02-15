# Poglink
[![codecov](https://codecov.io/gh/FM-17/poglink/branch/main/graph/badge.svg?token=Y84IU5NAH0)](https://codecov.io/gh/FM-17/poglink)
![Code style](https://img.shields.io/badge/Code%20style-black-000000)
![GitHub branch checks state](https://img.shields.io/github/checks-status/FM-17/poglink/main)
![GitHub issues](https://img.shields.io/github/issues/fm-17/poglink)
![GitHub pull requests](https://img.shields.io/github/issues-pr/fm-17/poglink)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/fm-17/poglink)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/poglink)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/poglink)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/fm-17/poglink)
![GitHub last commit](https://img.shields.io/github/last-commit/fm-17/poglink)


Poglink is a locally-hosted bot that monitors the ARK Web API and posts any changes to Discord. It was initially developed for use in the official [ARK: Survival Evolved Discord server](https://discord.gg/playark), but is open for anyone to use. 

## Server Rates Notifications
![image](https://i.ibb.co/2t9gR5K/poglink.png)

ARK's server rates are updated via [dynamic config URLs](https://arkdedicated.com/dynamicconfig.ini). When provided with these URLs, Poglink will automatically notify your Discord of any changes to the server rates.

Recently updated rates will be shown in **bold**, and the embed title will be automatically adjusted to indicate the game mode. If Poglink is set up in an [announcement channel](https://support.discord.com/hc/en-us/articles/360032008192-Announcement-Channels-), it will publish its messages so you don't have to.

## Getting Started 
- [Prerequisites](https://github.com/FM-17/poglink/blob/main/docs/prerequisites.md)
- [Running natively in Python](https://github.com/FM-17/poglink/blob/main/docs/native-installation.md)
- [Running within Docker container](https://github.com/FM-17/poglink/blob/main/docs/docker-installation.md)
- [Installing as a `systemd` Service](https://github.com/FM-17/poglink/blob/main/docs/systemd-installation.md)
- [Configuration](https://github.com/FM-17/poglink/blob/main/docs/configuration.md)

## Future updates
- ~~Delay between change detection and posting to discord~~ ✅
- Option to disable auto-publishing in announcement channels
- Optional in-game server notification integration
- Custom API endpoint selection for rates
- Optional ban summary integration
- Bot setup workflow in Discord
- Platform selection

> _📝 The developers of this bot are not affiliated with ARK: Survival Evolved or Studio Wildcard._
