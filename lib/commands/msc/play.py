import asyncio
import discord
from settings import *
from discord.ext import commands


@bot.command(name="play")
async def _play(cmd, *, query):
    if cmd.author.voice is None:
        await cmd.send("Please join a voice channel first.")
    else:
        tracks = await bot.wavelink.get_tracks(f"ytsearch:{query}")
        if not tracks:
            return await cmd.send(f"No matching query for {query}")
        player = bot.wavelink.get_player(cmd.guild.id)
        channel = cmd.author.voice.channel
        if not player.is_connected:
            await player.connect(channel.id)
            await cmd.send(f"Connected to {channel}")
        await player.play(tracks[0])
        

@_play.error
async def play_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")
