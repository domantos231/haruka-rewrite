import discord
from copy import deepcopy
from settings import *


@bot.command(name="queue")
async def _queue(cmd):
    if not cmd.author.voice:
        await cmd.send("Please join a voice channel first.")
    else:
        channel = cmd.author.voice.channel
        if channel.id not in queue:
            await cmd.send("Please add a song to queue.")
        else:
            em = discord.Embed(title=f"Music queue of channel {channel}", color=0x2ECC71)
            counter = 0
            tracks = []
            queue[channel.id].task_done()
            while not queue[channel.id].empty() and (track := queue[channel.id].get_nowait()) is not None:
                counter += 1
                em.add_field(name=f"**#{counter}** {track.title}", value=track.author, inline=False)
                tracks.append(track)
            for track in tracks:
                queue[channel.id].put_nowait(track)
            em.set_footer(text=f"Currently has {counter} song(s)")
            await cmd.send(embed=em)