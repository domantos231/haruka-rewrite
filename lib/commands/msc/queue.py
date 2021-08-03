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
            counter = 1
            queue[channel.id].task_done()
            tracks = deepcopy(queue[channel.id])
            while not tracks.empty() and (track := await tracks.get()) is not None:
                tracks.task_done()
                em.add_field(name=f"**#{counter}** {track.title}", value=track.author)
                counter += 1
            em.set_footer(text=f"Currently has {queue[channel.id].qsize()} song(s)")
            await cmd.send(embed=em)