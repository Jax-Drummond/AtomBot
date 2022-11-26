import datetime

import disnake
import disnake as discord

from config import *
from disnake.ext import commands
from printscreen import *

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


@bot.slash_command(description="Scrapes a random image from Prnt.sc")
async def prntsc(inter):
    embed = disnake.Embed(
        title="Print-screen Image",
        color=disnake.Color.blue(),
        timestamp=datetime.datetime.now(),
    )
    image = get_image()
    embed.set_image(file=disnake.File(image))
    print(embed.image)
    await inter.response.send_message(embed=embed)
    delete_photos()


bot.run(TOKEN)
