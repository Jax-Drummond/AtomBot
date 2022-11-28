import datetime

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

emoji = "<:thisisfine:1037528305202634792>"

custom_activity = discord.CustomActivity(
    name="Poop",
    type=discord.ActivityType.custom,
    emoji=emoji,
)

bot = commands.InteractionBot(
    command_sync_flags=command_sync_flags,
    intents=intents,
    activity=custom_activity,

)


@bot.event
async def on_ready():
    print("running")
    print(f'Logged in as {bot.user}')


@bot.slash_command(description="Test Command that responds with 'World'")
async def ping(inter):
    await inter.response.send_message("Pong")


@bot.slash_command(description="Scrapes a random image from Prnt.sc")
async def prntsc(inter: discord.ApplicationCommandInteraction):
    embed = discord.Embed(
        title="Print-screen Image",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.now(),
    )
    image = get_image()
    embed.set_image(file=discord.File(image))
    await inter.response.send_message(embed=embed,components=[
        discord.ui.Button(label="Again",style=discord.ButtonStyle.blurple,custom_id="Again")
    ])
    delete_photos()

    @bot.event
    async def on_button_click(inter: discord.MessageInteraction):
        if inter.component.custom_id == "Again":
            await prntsc(inter)

bot.run(TOKEN)

