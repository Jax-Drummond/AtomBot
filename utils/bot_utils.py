import os


# Gets all python files in the cogs directory and loads them as extensions
def load_cogs(bot, reload: bool = False):
    cog_dir = "cogs"

    bot.load_extensions(cog_dir)
