import asyncio

import disnake as discord
from disnake.ext import commands

from utils.bot_utils import load_cogs
from utils.pterodactyl_api import *


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

    @commands.slash_command(description="Get the status of a server", name="server-status", auto_sync=True)
    async def get_server_status(self, inter, server: str = commands.Param(choices=get_servers().keys())):
        servers = get_servers()
        await inter.response.send_message(
            f"The current status of {server} is {await get_server_status(servers[server])}")

    @commands.slash_command(description="Sends server power command", name="signal-server", auto_sync=True)
    @commands.default_member_permissions(administrator=True)
    async def control_server_power(self, inter,
                                   signal: str = commands.Param(choices=["start", "stop", "restart", "kill"]),
                                   server: str = commands.Param(choices=get_servers().keys())):
        servers = get_servers()
        await change_power_state(servers[server], signal)
        await inter.response.defer()

        if signal == "start" or signal == "restart":
            await inter.followup.send(f"The {server} server is now Starting")
            while await get_server_status(servers[server]) != "ONLINE":
                await asyncio.sleep(1)
        if signal == "stop" or signal == "kill":
            await inter.followup.send(f"The {server} server is now Stopping")
            while await get_server_status(servers[server]) != "OFFLINE":
                await asyncio.sleep(1)
        await inter.edit_original_response(
            f"The {server} server is now {await get_server_status(servers[server])}")


def setup(bot):
    bot.add_cog(Misc_Slash_Commands(bot))
