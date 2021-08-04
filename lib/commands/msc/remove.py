import discord
from settings import *


@bot.command(name="remove")
async def _remove(cmd):
    if not cmd.author.voice:
        await cmd.send("Please join a voice channel first.")
    else:
        channel = cmd.author.voice.channel
        if queue[channel.id].empty():
            await cmd.send("This channel does not have any songs in its queue to remove!")
        else:
            track = queue[channel.id].get_nowait()
            em = discord.Embed(title=track.title, description=track.author, color=0x2ECC71)
            em.set_author(name=f"{cmd.author.name} removed 1 song from channel {channel}", icon_url=cmd.author.avatar_url)
            await cmd.send(embed=em)