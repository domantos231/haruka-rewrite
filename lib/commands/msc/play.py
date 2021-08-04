import asyncio
import discord
from settings import *


@bot.command(name="play")
async def _play(cmd):
    if not cmd.author.voice:
        await cmd.send("Please join a voice channel first.")
    else:
        channel = cmd.author.voice.channel
        if queue[channel.id].empty():
            return await cmd.send("Please add at least one song to the queue.")
        player = bot.wavelink.get_player(guild_id=cmd.guild.id)
        if not player.channel_id:
            await player.connect(channel.id)
            await cmd.send(f"Connected to **{channel}**")
        elif not player.channel_id == channel.id:
            return await cmd.send(f"I'm currently playing in another voice channel! Consider using `{cmd.prefix}stop`.")
        while not queue[channel.id].empty() and player.is_connected:
            track = await queue[channel.id].get()
            em = discord.Embed(title=track.title, description=track.author, color=0x2ECC71)
            em.set_author(name=f"Playing in {channel}")
            em.set_thumbnail(url=track.thumb)
            await cmd.send(embed=em)
            await player.play(track)
            while player.is_playing:
                await asyncio.sleep(0.5)
        await player.disconnect()
