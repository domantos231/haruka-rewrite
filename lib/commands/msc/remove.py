import discord
from settings import *
from discord.ext import commands


@bot.command(
    name = "remove",
    description = "Remove a track from the current queue",
    usage = "remove <track position | default: 1>"
)
@commands.cooldown(1, 5, commands.BucketType.guild)
async def _remove(cmd, n: int = 1):
    if not cmd.author.voice:
        await cmd.send("Please join a voice channel first.")
    else:
        channel = Music(cmd.author.voice.channel)
        track = await channel.remove(n)
        if track:
            em = discord.Embed(title=track.title, description=track.author, url=track.uri, color=0x2ECC71)
            em.set_author(name=f"{cmd.author.name} removed 1 song from channel {channel.channel}", icon_url=cmd.author.avatar_url)
            em.set_thumbnail(url=track.thumb)
            await cmd.send(embed=em)
        else:
            await cmd.send("No song with this position.")
