from disnake.ext import commands
import disnake as discord

import config
from utils.classes.private_channel import Private_Channel
from utils.database_handler import get_all_records, remove_channel_record


class Private_Channels(commands.Cog):

    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        self.allowed_roles = [900094202816372746, 658493803073634304, 602668901452611590, 595460458421420060,
                              1055268820048162867]

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        private_channel: Private_Channel = Private_Channel.find_channel(channel=channel)
        if private_channel is not None:
            await private_channel.delete(f"{private_channel.member.mention}, Your private channel has been deleted.")

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.guilds[0]
        private_channel_records = await get_all_records()

        for channel_record in private_channel_records:
            channel_owner = guild.get_member(int(channel_record[0]))
            channel = guild.get_channel(int(channel_record[1]))
            if channel is not None:
                Private_Channel(channel_owner, channel)
                await self.on_raw_member_update(channel_owner)
            else:
                await remove_channel_record(channel_record[1])

    @commands.Cog.listener()
    async def on_raw_member_update(self, member: discord.Member):
        private_channel: Private_Channel = Private_Channel.find_channel(member=member)
        if private_channel is not None:
            is_allowed = await self.is_allowed_channel(member)

            if not is_allowed and len(member.roles) > 1:
                await private_channel.delete(
                    f"{member.mention}, You are no longer a server booster. Your private channel has been deleted."
                )

    async def is_allowed_channel(self, user: discord.Member) -> bool:
        for role in self.allowed_roles:
            is_allowed = user.get_role(role) is not None
            if is_allowed:
                return True
        return False

    @commands.slash_command(description="Creates a private vc for you. Must be a server booster or council member.",
                            name="create-private-vc")
    async def create_private_vc(self, inter: discord.MessageCommandInteraction, name: str = None):

        category_id = config.VC_CATEGORY
        command_user = inter.user

        is_allowed = await self.is_allowed_channel(command_user)

        if is_allowed is True:
            private_channel: Private_Channel = Private_Channel.find_channel(member=command_user)
            if private_channel is None:
                name = name if name is not None else f"{command_user.name}'s VC"
                new_vc = await command_user.guild.get_channel(category_id).create_voice_channel(name)
                await new_vc.set_permissions(target=command_user,
                                             view_channel=True,
                                             manage_channels=True,
                                             manage_permissions=True,
                                             )
                await Private_Channel.new(command_user, new_vc)
                await inter.response.send_message("Channel created.", ephemeral=True, delete_after=2)
            else:
                await inter.response.send_message("You already have a channel silly.", ephemeral=True,
                                                  delete_after=2)
        else:
            await inter.response.send_message("You are not a booster of the server. ;(", ephemeral=True, delete_after=2)

    @commands.slash_command(
        description="Adds a record.",
        name="add_private_record")
    @commands.default_member_permissions(administrator=True)
    async def add_private_channel_record(self, inter: discord.MessageCommandInteraction,
                                         channel: discord.VoiceChannel,
                                         action: str = commands.Param(choices=["add", "remove"]),
                                         user: discord.Member = None,
                                         ):
        if action == "add" and user is not None and channel is not None:
            await Private_Channel.new(user, channel)
            await inter.response.send_message("Record added.", ephemeral=True, delete_after=2)
        elif action == "remove" and channel is not None:
            await remove_channel_record(channel.id)
            await inter.response.send_message("Record deleted.", ephemeral=True, delete_after=2)
        else:
            await inter.response.send_message(
                "Must provide channel and user for adding, and just channel for removing.", ephemeral=True,
                delete_after=2)


def setup(bot):
    bot.add_cog(Private_Channels(bot))
