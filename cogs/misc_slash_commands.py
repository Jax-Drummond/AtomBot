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

    @commands.slash_command(description="Get status of a server")
    async def get_server_status(self, inter, server: str = commands.Param(choices=get_servers().keys())):
        servers = get_servers()
        await inter.response.send_message(f"Status of {server} is {await get_server_status(servers[server])}")


def setup(bot):
    bot.add_cog(Misc_Slash_Commands(bot))
