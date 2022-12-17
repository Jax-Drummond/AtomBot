import disnake as discord

from utils.bot_logging import initialize_logging
from config import *
from disnake.ext import commands
from utils.bot_utils import load_cogs

token = None
if ENVIRONMENT == "PROD":
    token = TOKEN
else:
    token = DEV_TOKEN

# Sets up command sync flags
command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

# Sets up intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Creates the Bot
bot = commands.InteractionBot(
    command_sync_flags=command_sync_flags,
    intents=intents,

)

# Initializes bot logging for debugging
initialize_logging()

# Loads Cogs
load_cogs(bot)

# bot.add_cog(ButtonRoles(bot))
# Runs the bot
bot.run(token)
