import disnake as discord
from config import *
from disnake.ext import commands

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True

bot = commands.InteractionBot(
    command_sync_flags=command_sync_flags,
    intents=intents,
)


@bot.event
async def on_ready():
    print("running")
    print(f'Logged in as {bot.user}')


@bot.slash_command(description="Test Command that responds with 'World'")
async def hello(inter):
    await inter.response.send_message("World")


bot.run(TOKEN)
