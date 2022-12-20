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

    @commands.slash_command(description="Get the status of a server", name="server-status")
    async def get_server_status(self, inter, server: str = commands.Param(choices=get_servers().keys())):
        servers = get_servers()
        await inter.response.send_message(
            f"The current status of {server} is {await get_server_status(servers[server])}")

    @commands.slash_command(description="Sends server power command", name="signal-server")
    @commands.default_member_permissions(administrator=True)
    async def control_server_power(self, inter,
                                   signal: str = commands.Param(choices=["start", "stop", "restart", "kill"]),
                                   server: str = commands.Param(choices=get_servers().keys())):
        servers = get_servers()
        await change_power_state(servers[server], signal)
        await inter.response.defer()
        await asyncio.sleep(3)
        await inter.followup.send(
            f"The current status of {server} is {await get_server_status(servers[server])}")


def setup(bot):
    bot.add_cog(Misc_Slash_Commands(bot))
