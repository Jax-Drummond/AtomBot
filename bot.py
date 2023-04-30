import disnake as discord
import wavelink
from disnake.ext import commands

from config import *
from utils.bot_logging import initialize_logging
from utils.bot_utils import load_cogs

from utils.pterodactyl_api import get_servers

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
intents.members = True

activity = discord.Activity(name="The Consultant", type=discord.ActivityType.watching)

# Creates the Bot
bot = commands.InteractionBot(
    command_sync_flags=command_sync_flags,
    intents=intents,
    activity=activity,
)

# Initializes bot logging for debugging
initialize_logging()

# Gets PteroSERVERS
get_servers()

# Loads Cogs
load_cogs(bot)

# Runs the bot
bot.run(token)
