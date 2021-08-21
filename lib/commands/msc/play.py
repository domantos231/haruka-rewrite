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
        await channel.connect()
        loop = "loop" in args
        verbose = "verbose" in args
        status = ""
        if loop:
            status += "**Loop**: ON | Any started songs will be added back to the queue.\n"
        else:
            status += "**Loop**: OFF"
        if verbose:
            status += "**Verbose**: ON | Song details will be displayed before playing.\n"
        else:
            status += "**Verbose**: OFF"
        await cmd.send(f"Connected to **{channel.channel}**\n{status}")
        while len(queue) > 0 and channel.player.is_connected():
            track = await channel.remove(1)
            if loop:
                await channel.add(track)
            if verbose:
                em = discord.Embed(title=track.title, description=track.author, url=track.uri, color=0x2ECC71)
                em.set_author(name=f"Playing in {channel.channel}")
                em.set_thumbnail(url=track.thumb)
                await cmd.send(embed=em)
            try:
                await channel.play(track)
            except AttributeError:
                return
            queue = await channel.queue
        await channel.player.disconnect()
