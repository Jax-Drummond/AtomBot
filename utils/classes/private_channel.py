import disnake as discord

from utils.database_handler import remove_channel_record, add_user_channel


class Private_Channel:
    private_channels = []

    def __init__(self, member: discord.Member, channel: discord.VoiceChannel):
        print("Private Channel object created.")
        Private_Channel.private_channels.append(self)
        self.private_channels = Private_Channel.private_channels
        self.member = member
        self.channel = channel

    # Creates a new record on the database and returns a Private_Channel object
    @classmethod
    async def new(cls, member: discord.Member, channel: discord.VoiceChannel):
        await add_user_channel(member.id, channel.id)
        return cls(member, channel)

    async def delete(self, reason: str = None):
        reason = "Channel deleted by bot." if reason is None else reason
        Private_Channel.private_channels.remove(self)
        self.private_channels = Private_Channel.private_channels
        try:
            await self.channel.delete(reason=reason)
        except:
            print("Channel already deleted")
        await self.member.send(reason, delete_after=120)
        await remove_channel_record(self.channel.id)

    @staticmethod
    def find_channel(member: discord.Member = None, channel: discord.VoiceChannel = None):
        if member is not None:
            for private_channel in Private_Channel.private_channels:
                if private_channel.member == member:
                    return private_channel
        elif channel is not None:
            for private_channel in Private_Channel.private_channels:
                if private_channel.channel == channel:
                    return private_channel
        return None
