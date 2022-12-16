import asyncio
import datetime

import disnake as discord

from botlogging import initialize_logging
from config import *
from disnake.ext import commands
from printscreen import *

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


# Event Listener for when the bot is ready
# Tells us that the bot is running
@bot.event
async def on_ready():
    print("running")
    print(f'Logged in as {bot.user}')
    delete_photos()


# Creates the /ping Command
# Responds with "Pong"
@bot.slash_command(description="Test Command that responds with 'Pong'")
async def ping(inter):
    await inter.response.send_message("Pong")


@bot.event
async def on_message_command_error(inter, error):
    print(f"{error} This is the error.")


# Creates the /prntsc Command
# Gets a random image from https://prnt.sc
@bot.slash_command(description="Scrapes a random image from Prnt.sc")
async def prntsc(inter: discord.ApplicationCommandInteraction):
    # Builds the Embed
    embed = discord.Embed(
        title="Print-screen Image",
        color=discord.Color.blue(),
        type="image",
        timestamp=datetime.datetime.now(),
    )
    # Gets image from prnt.sc
    image = get_image()
    # Set the image of the embed to the one we got from prnt.sc
    embed.set_image(file=discord.File(image))
    await inter.response.defer()

    # Sends a message embed that has a button
    await inter.followup.send(embed=embed, components=[
        discord.ui.Button(label="Again", style=discord.ButtonStyle.blurple, custom_id="Again")
    ])


# Event listener for when a button is clicked
@bot.event
async def on_button_click(inter: discord.MessageInteraction):
    guild = inter.guild
    user = inter.user
    # This is for the Again button on /prnt.sc
    if inter.component.custom_id == "Again":
        await prntsc(inter)

    # This is for the /button_role command
    if inter.component.label == "Get/Remove Role":
        role = guild.get_role(int(inter.component.custom_id))
        await inter.response.defer()
        try:
            if user.get_role(int(inter.component.custom_id)) is None:
                await user.add_roles(role)
                await inter.send(f"{role.mention} was Added", ephemeral=True, delete_after=5)
            else:
                await user.remove_roles(role)
                await inter.send(f"{role.mention} was Removed", ephemeral=True, delete_after=5)
        except discord.HTTPException:
            await inter.send("There was an error. Please try again in a few minutes.", ephemeral=True, delete_after=15)


# Creates the /button_roles command
# Allows the user to send an embed with a button
# that when clicked adds or removes a role
@bot.slash_command(description="Create a button role with Message")
# Sets the slash command perms to administrator only
@commands.default_member_permissions(administrator=True)
async def button_roles(inter, role: discord.Role, description: commands.String[0, 200],
                       channel: discord.TextChannel = None):
    embed = discord.Embed(
        title="Get Role",
        colour=role.color,
        description=f"Click on the button below to get the ***{role.mention}*** role.",
    )
    embed.add_field(name="Description", value=description, inline=False)
    if channel is None:
        await inter.response.send_message(embed=embed, components=[
            discord.ui.Button(label="Get/Remove Role", style=discord.ButtonStyle.blurple, custom_id=f"{role.id}")
        ])
    else:
        await channel.send(embed=embed, components=[
            discord.ui.Button(label="Get/Remove Role", style=discord.ButtonStyle.blurple, custom_id=f"{role.id}")
        ])
        await inter.send("Button role successfully created", ephemeral=True, delete_after=2)


# Initializes bot logging for debugging
initialize_logging()

# Runs the bot
bot.run(TOKEN)
