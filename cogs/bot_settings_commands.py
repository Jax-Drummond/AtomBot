import disnake as discord

from disnake.ext import commands


class Bot_Settings_Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="set-bot-activity",
        description="Changes the bots discord activity.",
        auto_sync=True,
        install_types=discord.ApplicationInstallTypes.all(),
        contexts=discord.InteractionContextTypes.all(),
    )
    @commands.default_member_permissions()
    async def set_bot_activity(
            self,
            inter,
            activity_text: str,
            activity_type: discord.ActivityType,
            activity_status: discord.Status = None
    ):
        if await self.bot.is_owner(inter.user):

            if activity_type == 1:
                new_activity = discord.Streaming(
                    name=activity_text,
                    url="https://www.twitch.tv/atomicbombg0d"
                )
            else:
                new_activity = discord.Activity(
                    name=activity_text,
                    type=activity_type
                )

            await self.bot.change_presence(
                activity=new_activity,
                status=activity_status
            )
            await inter.send(
                f"Activity set to {activity_text}",
                ephemeral=True,
                delete_after=2
            )
        else:
            await inter.send(
                "Hello? You aren't the bot owner!",
                ephemeral=True,
                delete_after=2
            )


def setup(bot):
    bot.add_cog(Bot_Settings_Commands(bot))
