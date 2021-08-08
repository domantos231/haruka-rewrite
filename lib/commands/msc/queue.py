import discord
from settings import *
from discord.ext import commands


async def get_track(index, track_id):
    track = await bot.wavelink.build_track(track_id)
    return index, track_id


def sort_by_index(obj):
    return obj[0]


@bot.command(name="queue")
@commands.cooldown(1, 5, commands.BucketType.guild)
async def _queue(cmd):
    if not cmd.author.voice:
        await cmd.send("Please join a voice channel first.")
    else:
        channel = cmd.author.voice.channel
        row = await bot.db.conn.fetchrow(f"SELECT * FROM music WHERE id = '{channel.id}';")
        if not row:
            track_ids = []
        else:
            track_ids = row["queue"]
        em = discord.Embed(title=f"Music queue of channel {channel}", color=0x2ECC71)
        counter = 0
        for track_id in track_ids:
            track = await bot.wavelink.build_track(track_id)
            counter += 1
            em.add_field(name=f"**#{counter}** {track.title}", value=track.author, inline=False)
        em.set_footer(text=f"Currently has {counter} song(s)")
        await cmd.send(embed=em)