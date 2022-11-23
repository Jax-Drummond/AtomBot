import disnake as discord
from config import *
from disnake.ext import commands



command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = True

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.reactions = True
client = discord.Client(intents=intents)



@client.event
async def on_ready():
    print(f'Logged on as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(f'Message from {message.author}: {message.content} in {message.channel.id}')


bot = commands.Bot(
    command_prefix='..',
    command_sync_flags=command_sync_flags,
    intents=intents,
)


@bot.slash_command(description="Test Command that responds with 'World'")
async def aloha(inter):
    await inter.response.send_message("World")


bot.run(TOKEN)
