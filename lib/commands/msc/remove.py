import discord
from settings import *
from discord.ext import commands


@bot.command(name="remove")
@commands.cooldown(1, 5, commands.BucketType.guild)
async def _remove(cmd, n: int = 1):
    if not cmd.author.voice:
        await cmd.send("Please join a voice channel first.")
    else:
        channel = cmd.author.voice.channel
        row = await bot.db.conn.fetchrow(f"SELECT * FROM music WHERE id = '{channel.id}';")
        if not row or len(row["queue"]) == 0:
            await cmd.send("This channel does not have any songs in its queue to remove!")
        elif len(row["queue"]) < n:
            raise commands.UserInputError
        else:
            track_id = row["queue"][n - 1]
            await bot.db.conn.execute(f"UPDATE music SET queue = array_cat(queue[:{n - 1}], queue[{n + 1}:]) WHERE id = '{channel.id}';")
            track = await bot.wavelink.build_track(track_id)
            em = discord.Embed(title=track.title, description=track.author, color=0x2ECC71)
            em.set_author(name=f"{cmd.author.name} removed 1 song from channel {channel}", icon_url=cmd.author.avatar_url)
            em.set_thumbnail(url=track.thumb)
            await cmd.send(embed=em)


@_remove.error
async def remove_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again")