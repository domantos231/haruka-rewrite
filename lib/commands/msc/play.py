import asyncio
import discord
from datetime import datetime as dt
from discord.ext import commands
from settings import *


@bot.command(name="play")
@commands.cooldown(1, 5, commands.BucketType.guild)
async def _play(cmd, *args):
    if not cmd.author.voice:
        await cmd.send("Please join a voice channel first.")
    else:
        channel = Music(cmd.author.voice.channel)
        queue = await channel.queue
        if len(queue) == 0:
            return await cmd.send("Please add a song to the queue.")
        vc = await channel.connect()
        await cmd.send(f"Connected to **{channel._channel}**")
        if "loop" in args:
            await cmd.send("Playing the current queue in a loop. Any started song will be added back to the queue.")
            loop = True
        else:
            loop = False
        if "verbose" in args:
            await cmd.send("Playing in verbose mode. Songs will be displayed before starting.")
            verbose = True
        else:
            verbose = False
        while len(queue) > 0 and channel.is_connected():
            video_id = await channel.remove(1)
            if loop:
                await channel.add(video_id)
            if verbose:
                em = discord.Embed(title=track.title, description=track.author, url=track.uri, color=0x2ECC71)
                em.set_author(name=f"Playing in {channel.channel}")
                em.set_thumbnail(url=track.thumb)
                await cmd.send(embed=em)
            try:
                buffer_url = await bot.buffer(video_id)
                await channel.play(buffer_url)
            except AttributeError:
                return
            queue = await channel.queue
        await channel.disconnect()
