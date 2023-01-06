import asyncio

import disnake as discord
from disnake.ext import commands

from utils.pterodactyl_api import *


class Ptero_Slash_Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.selected_server = [""]

    @commands.Cog.listener()
    async def on_dropdown(self, inter: discord.MessageInteraction):
        check = commands.has_permissions(administrator=True).predicate
        if inter.component.custom_id == "server.select":
            try:
                await check(inter)
            except discord.ext.commands.errors.MissingPermissions:
                return
            self.selected_server = inter.values
            await inter.send("Server selected", ephemeral=True, delete_after=2)

    @commands.Cog.listener()
    async def on_button_click(self, inter: discord.MessageInteraction):
        states = ["start", "stop", "restart", "kill"]
        # This is for the Again button on /prnt.sc
        check = commands.has_permissions(administrator=True).predicate

        if states.__contains__(inter.component.custom_id):
            try:
                await check(inter)
            except discord.ext.commands.errors.MissingPermissions:
                await inter.response.send_message("You do not have the required permissions.", ephemeral=True,
                                                  delete_after=3)
                return
            signal = inter.component.custom_id
            server = self.selected_server[0]
            if self.selected_server[0] != "":
                await change_power_state(server, signal)
                await inter.response.defer()
                if signal in ("start", "restart"):
                    await inter.followup.send(f"Waiting to updated embed", ephemeral=True, delete_after=2)
                    while await get_server_status(server) != server_states["running"]:
                        await asyncio.sleep(1)
                else:
                    await inter.followup.send(f"Waiting to updated embed", ephemeral=True, delete_after=2)
                    while await get_server_status(server) != server_states["offline"]:
                        await asyncio.sleep(1)
                embed = await servers_embed()
                self.selected_server[0] = ""
                await inter.message.edit(embed=embed)
            else:
                await inter.send("No server selected", ephemeral=True, delete_after=2)

    @commands.slash_command(name="ptero-server")
    async def ptero_server(self, inter):
        pass

    @commands.slash_command(name="ptero-server-a")
    @commands.default_member_permissions(administrator=True)
    async def ptero_server_admin(self, inter):
        pass

    # Creates the /ptero-server status command
    # Gets the status of the server on pterodactyl
    @ptero_server.sub_command(description="Get the status of a server", name="status", auto_sync=True)
    async def get_server_status(self, inter, server: str = commands.Param(choices=servers.keys())):
        await inter.response.send_message(
            f"The current status of {server} is {await get_server_status(servers[server])}")

    # Creates the /ptero-server signal command
    # Allows the user to send a signal to the server to start, stop, restart, and kill
    @ptero_server_admin.sub_command(description="Sends server power command", name="signal", auto_sync=True)
    async def control_server_power(self, inter: discord.ApplicationCommandInteraction,
                                   signal: str = commands.Param(choices=["start", "stop", "restart", "kill"]),
                                   server: str = commands.Param(choices=servers.keys())):
        await change_power_state(servers[server], signal)
        await inter.response.defer()

        if signal in ("start", "restart"):
            await inter.followup.send(f"The {server} server is now STARTING")
            while await get_server_status(servers[server]) != server_states["running"]:
                await asyncio.sleep(1)
        else:
            await inter.followup.send(f"The {server} server is now STOPPING")
            while await get_server_status(servers[server]) != server_states["offline"]:
                await asyncio.sleep(1)

        await inter.edit_original_response(
            f"The {server} server is now {await get_server_status(servers[server])}")

    @ptero_server_admin.sub_command(description="Creates a status embed for the servers", name="status-embed",
                                    auto_sync=True)
    async def status_embed(self, inter: discord.ApplicationCommandInteraction,
                           channel: discord.TextChannel | discord.ForumChannel | None = None):
        await inter.response.send_message("Hang tight, embed being created.", ephemeral=True, delete_after=1)
        embed = await servers_embed()
        view = discord.ui.View()
        select = discord.ui.StringSelect(custom_id="server.select", placeholder="Server", max_values=1, min_values=1)

        for s in servers:
            select.add_option(label=s, value=servers[s])

        view.add_item(select)
        view.add_item(discord.ui.Button(label="Start", style=discord.ButtonStyle.success, custom_id="start"))
        view.add_item(discord.ui.Button(label="Stop", style=discord.ButtonStyle.danger, custom_id="stop"))
        view.add_item(discord.ui.Button(label="Kill", style=discord.ButtonStyle.danger, custom_id="kill"))
        view.add_item(discord.ui.Button(label="Restart", style=discord.ButtonStyle.blurple, custom_id="restart"))
        if channel is not None:
            await channel.send(embed=embed, view=view)
        else:
            await inter.channel.send(embed=embed, view=view)


def setup(bot):
    bot.add_cog(Ptero_Slash_Commands(bot))
