from disnake.ext import commands

from utils.print_screen import *


class Event_Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Event Listener for when the bot is ready
    # Tells us that the bot is running
    @commands.Cog.listener()
    async def on_ready(self):
        await delete_photos()
        print(f'Logged in as {self.bot.user}')


def setup(bot):
    bot.add_cog(Event_Handler(bot))
