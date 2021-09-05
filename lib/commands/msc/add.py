import asyncio
import discord
import wavelink
from settings import *
from discord.ext import commands


@bot.command(
    name = "add",
    description = "Search for a YouTube track and add to queue.",
    usage = "add <query>",
)
@commands.cooldown(1, 5, commands.BucketType.guild)
async def _add(cmd, *, query):
    if not cmd.author.voice:
        await cmd.send("Please join a voice channel first.")
    else:
        channel = Music(cmd.author.voice.channel)
        queue = await channel.queue
        if len(queue) >= 30:
            return await cmd.send("The music queue for this channel has reached its maximum size.")
        tracks = await wavelink.YouTubeTrack.search(query=query)
        if tracks:
            em = discord.Embed(
                title = f"Search results for {query}",
                color = 0x2ECC71,
            )
            em.set_author(
                name = f"{cmd.author.name}'s song request",
                icon_url = cmd.author.avatar.url if cmd.author.avatar else None,
            )
            em.set_footer(text = "This messagge will expire after 5 minutes.")
            for obj in enumerate(tracks[:6]):
                track = obj[1]
                em.add_field(
                    name = f"{choices[obj[0]]} {track.title}",
                    value = track.author,
                    inline = False,
                )
            msg = await cmd.send(embed=em)
        else:
            return await cmd.send(f"No matching result for {query}")
        length = len(tracks)
        for choice in choices[:length]:
            await msg.add_reaction(choice)
        

        def check(reaction, user):
            return user.id == cmd.author.id and reaction.message.id == msg.id and str(reaction) in choices[:length]
        

        try:
            reaction, user = await bot.wait_for("reaction_add", check=check, timeout=300.0)
        except asyncio.TimeoutError:
            return await msg.reply(f"<@!{cmd.author.id}> didn't respond to the queue. Request timed out")
        else:
            index = choices.index(str(reaction))
            track = tracks[index]
            await channel.add(track)
            em = discord.Embed(title=track.title, description=track.author, url=track.uri, color=0x2ECC71)
            em.set_author(
                name = f"{cmd.author.name} added 1 song to queue",
                icon_url = cmd.author.avatar.url if cmd.author.avatar else None,
            )
            em.set_thumbnail(url=track.thumb)
            await msg.delete()
            await cmd.send(embed=em)
