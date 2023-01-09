import datetime

import disnake as discord
from disnake.ext import commands

from utils.bot_utils import load_cogs
from utils.chicopee_work_sched import work_embed
from utils.print_screen import get_image
import requests


class Misc_Slash_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Creates the /reload Command
    # Reloads the bots cogs
    @commands.slash_command(description="Reloads the bots cogs")
    @commands.default_member_permissions(administrator=True)
    async def reload(self, inter: discord.ApplicationCommandInteraction):
        load_cogs(self.bot, True)
        await inter.response.send_message("Reloaded cogs.", ephemeral=True, delete_after=5)

    @commands.Cog.listener()
    async def on_button_click(self, inter: discord.MessageInteraction):
        # This is for the Again button on /prnt.sc
        if inter.component.custom_id == "Again":
            await self.prntsc(inter)
        if inter.component.label == "Refresh":
            name = inter.component.custom_id
            url = inter.message.embeds[0].url
            embed = work_embed(url, name)
            await inter.response.defer()
            await inter.message.edit(embed=embed)

    # Creates the /prntsc Command
    # Gets a random image from https://prnt.sc
    @commands.slash_command(description="Scrapes a random image from Prnt.sc")
    async def prntsc(self, inter: discord.ApplicationCommandInteraction):
        try:
            await inter.response.defer(with_message=True)
            # Builds the Embed
            embed = discord.Embed(title="Print-screen Image", color=discord.Color.blue(),
                                  timestamp=datetime.datetime.now())
            # Gets image from prnt.sc
            image = await get_image()
            # Set the image of the embed to the one we got from prnt.sc
            embed.set_image(file=discord.File(image))

            # Sends a message embed that has a button
            await inter.followup.send(embed=embed, components=[
                discord.ui.Button(label="Again", style=discord.ButtonStyle.blurple, custom_id="Again")
            ])
        except discord.errors.NotFound:
            await self.prntsc(inter)

    # Creates the /work_sched Command
    # Displays the work schedule(For Chicopee employees only)
    @commands.slash_command(description="Displays your work schedule (For Chicopee employees only)")
    async def work_sched(self, inter: discord.ApplicationCommandInteraction, url: str, name: str):
        embed = work_embed(url, name)
        await inter.response.send_message("Schedule sent", ephemeral=True, delete_after=3)
        await inter.user.send(embed=embed, components=[
            discord.ui.Button(label="Refresh", style=discord.ButtonStyle.gray, custom_id=f"{name}")
        ])

    @commands.slash_command(description="Get a picture of the hill", name="chic-o-peek-cam")
    async def chic_o_peek_cam(self, inter):
        await inter.response.defer()
        embed = discord.Embed(title="Chic-o-Peek Webcam", timestamp=datetime.datetime.now())
        response = requests.get("http://chicopeetubepark.com/webcam/camera.jpg", stream=True)

        if not response.ok:
            print(response)

        with open('images/camera.jpg', 'wb') as file:
            file.write(response.content)

        embed.set_image(file=discord.File('images/camera.jpg'))
        await inter.followup.send(embed=embed)

    @commands.message_command(name="Delete")
    async def delete_dm(self, inter: discord.MessageCommandInteraction, message: discord.Message):
        if message.author == self.bot.user and message.channel.type is None:
            await inter.response.send_message("Message deleted", ephemeral=True, delete_after=1)
            await message.delete()
        else:
            await inter.response.send_message("Must be used in a DM Channel and on a message created by the bot.",
                                              ephemeral=True, delete_after=5)
        print(f"{message.author}:{self.bot.user} {message.channel.type}")


def setup(bot):
    bot.add_cog(Misc_Slash_Commands(bot))
