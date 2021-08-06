import asyncio
import discord
from datetime import datetime as dt
from discord.ext import commands
from settings import *


@bot.command(name="play")
@commands.cooldown(1, 5, commands.BucketType.guild)
async def _play(cmd, arg = None):
    loop = False
    if not cmd.author.voice:
        await cmd.send("Please join a voice channel first.")
    else:
        channel = cmd.author.voice.channel
        if queue[channel.id].empty():
            return await cmd.send("Please add at least one song to the queue.")
        player = bot.wavelink.get_player(guild_id=cmd.guild.id)
        if not player.channel_id == channel.id:
            await player.connect(channel.id)
            await cmd.send(f"Connected to **{channel}**")
        if not arg:
            pass
        elif arg.lower() == "loop":
            await cmd.send("Playing the current queue in a loop, any completed songs will be added back to the queue.")
            loop = True
        else:
            raise commands.UserInputError
        while not queue[channel.id].empty() and player.is_connected:
            track = await queue[channel.id].get()
            if loop:
                await queue[channel.id].put(track)
            em = discord.Embed(title=track.title, description=track.author, color=0x2ECC71)
            em.set_author(name=f"Playing in {channel}")
            em.set_thumbnail(url=track.thumb)
            await cmd.send(embed=em)
            start = dt.now()
            await player.play(track)
            end = dt.now()
            if (end - start).seconds < 2:
                return await cmd.send("It seems that something went wrong with the server. Maybe try it again?") 
        await player.disconnect()


@_play.error
async def play_error(cmd, error):
    if isinstance(cmd, commands.UserInputError):
        await cmd.send(f"Valid argument after `{cmd.prefix}play` is `loop`")
