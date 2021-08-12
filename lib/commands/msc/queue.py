import asyncio
import discord
from settings import *
from discord.ext import commands


songs_per_page = 10
inline = True


@bot.command(name="queue")
@commands.cooldown(1, 10, commands.BucketType.guild)
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
        name = []
        value = []
        embed = []
        for track_id in track_ids:
            track = await bot.wavelink.build_track(track_id)
            name.append(f"**#{counter}** {track.title}")
            value.append(track.author)
        pages = 1 + int(len(track_ids)/songs_per_page)
        for page in range(pages):
            embed.append(discord.Embed(title=f"Music queue of channel {channel}", color=0x2ECC71))
            embed[page].set_footer(text=f"Currently has {len(track_ids)} song(s) | Page {page + 1}/{pages}")
            for i in range(songs_per_page):
                try:
                    embed[page].add_field(name=name[0], value=value[0], inline=inline)
                    del name[0], value[0]
                except AttributeError:
                    break
        msg = await cmd.send(embed=embed[0])
        for emoji in choices[:pages]:
            await msg.add_reaction(emoji)
        

        def check(reaction, user):
            return reaction.message.id == msg.id and str(reaction) in choices[:pages]
        

        async def active():
            while True:
                done, pending = await asyncio.wait([bot.wait_for("reaction_add", check=check),
                                                    bot.wait_for("reaction_remove", check=check)],
                                                    return_when = asyncio.FIRST_COMPLETED)
                reaction, user = done.pop().result()
                page = choices.index(str(reaction))
                await msg.edit(embed=embed[page])
        

        try:
            await asyncio.wait_for(active(), timeout=120.0)
        except asyncio.TimeoutError:
            return await msg.clear_reactions()