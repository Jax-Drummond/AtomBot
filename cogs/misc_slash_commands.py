import asyncio
import wave

import disnake as discord
import pyaudio as pyaudio
from disnake.ext import commands

from utils.bot_utils import load_cogs


async def record_audio(channel, duration):
    def callback(in_data, frame_count, time_info, status):
        frames.append(in_data)
        return (None, pyaudio.paContinue)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=48000, input=True, frames_per_buffer=1024,
                    stream_callback=callback)
    frames = []
    stream.start_stream()
    await asyncio.sleep(duration)
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open("recorded_audio.wav", "wb")
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(48000)
    wf.writeframes(b"".join(frames))
    wf.close()


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

    @commands.slash_command(description="Stuff")
    async def record(self, inter, duration: int | int = 10):
        channel = inter.author.voice.channel
        await channel.connect()
        await record_audio(channel, duration)
        await channel.disconnect()

    @commands.slash_command(description="Stuff2")
    async def play(self, inter):
        channel = inter.author.voice.channel
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio("recorded_audio.wav"))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 0.5
        await vc.disconnect()


def setup(bot):
    bot.add_cog(Misc_Slash_Commands(bot))
