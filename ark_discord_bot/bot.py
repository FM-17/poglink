from discord.ext import commands

class BotConfig:
    token = None, 
    rates_channel_id = None,
    bans_channel_id = None,
    polling_delay = None,
    allowed_roles = None,
    rates_url = None,
    bans_url = None,

class ConfigurableBot(commands.Bot):
    def __init__(self, command_prefix, config_dict, **kwargs):
        self.config = BotConfig()
        for k,v in config_dict.items():
            setattr(self.config, k, v)
        
        super().__init__(command_prefix, **kwargs)
        