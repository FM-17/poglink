# Poglink

Poglink is a locally-hosted bot that monitors the ARK Web API and posts any changes to Discord. It was initially developed for use in the official [ARK: Survival Evolved Discord server](https://discord.gg/playark), but is open for anyone to use. 

### **Server Rates Notifications**
![image](https://i.ibb.co/2t9gR5K/poglink.png)

ARK's server rates are updated via dynamic config URL's. For example, the "official" rates can be found at https://arkdedicated.com/dynamicconfig.ini. When provided with these URL's, `poglink` will automatically notify your Discord of any changes to the server rates.

Notes:
- Recently updated rates will be shown in **bold**
- Embed title will be adjusted automatically based on the game mode
- Server rates notifications will be published automatically if `poglink` is setup in an [announcement channel](https://support.discord.com/hc/en-us/articles/360032008192-Announcement-Channels-)



## Getting Started
- Prerequisites
- Running natively in Python
- Running within Docker container
- Configuration
- Troubleshooting

## Future updates
- Configurable delay between change detection and posting to discord
- Option to disable auto-publishing in announcement channels
- Optional in-game server notification integration
- Custom API endpoint selection for rates
- Optional ban summary integration
- Bot setup workflow in Discord
- Platform selection
