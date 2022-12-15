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

bot = commands.InteractionBot(
    command_sync_flags=command_sync_flags,
    intents=intents,

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
        type="image",
        timestamp=datetime.datetime.now(),
    )
    image = get_image()
    embed.set_image(file=discord.File(image))
    await inter.response.send_message(embed=embed, components=[
        discord.ui.Button(label="Again", style=discord.ButtonStyle.blurple, custom_id="Again")
    ])
    delete_photos()


@bot.event
async def on_button_click(inter: discord.MessageInteraction):
    guild = inter.guild
    user = inter.user
    if inter.component.custom_id == "Again":
        await prntsc(inter)
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


@bot.slash_command(description="Create a button role with Message")
@commands.default_member_permissions(administrator=True)
async def button_roles(inter, role: discord.Role, description: commands.String[0, 200]):
    embed = discord.Embed(
        title="Get Role",
        colour=role.color,
        description=f"Click on the button below to get the ***{role.mention}*** role.",
    )
    embed.add_field(name="Description", value=description, inline=False)
    await inter.response.send_message(embed=embed, components=[
        discord.ui.Button(label="Get/Remove Role", style=discord.ButtonStyle.blurple, custom_id=f"{role.id}")
    ])


bot.run(TOKEN)
