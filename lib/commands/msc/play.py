import asyncio
import discord
from datetime import datetime as dt
from discord.ext import commands
from settings import *


@bot.command(name="play")
@commands.cooldown(1, 5, commands.BucketType.guild)
async def _play(cmd, arg = None):
    loop = False
    if not cmd.author.voice:
        await cmd.send("Please join a voice channel first.")
    else:
        channel = cmd.author.voice.channel
        row = await bot.db.conn.fetchrow(f"SELECT * FROM music WHERE id = '{channel.id}';")
        if not row or len(row["queue"]) == 0:
            return await cmd.send("Please add at least one song to the queue.")
        queue = row["queue"]
        player = bot.wavelink.get_player(guild_id=cmd.guild.id)
        if not player.channel_id == channel.id:
            await player.connect(channel.id)
            await cmd.send(f"Connected to **{channel}**")
        elif player.is_connected:
            await cmd.send("Skipping to next song...")
        if not arg:
            pass
        elif arg.lower() == "loop":
            await cmd.send("Playing the current queue in a loop, any completed/skipped songs will be added back to the queue.")
            loop = True
        else:
            raise commands.UserInputError
        while len(queue) > 0 and player.is_connected:
            track_id = queue[0]
            await bot.db.conn.execute(f"UPDATE music SET queue = queue[2:] WHERE id = '{channel.id}';")
            if loop:
                await bot.db.conn.execute(f"UPDATE music SET queue = array_append(queue, '{track_id}') WHERE id = '{channel.id}';")
            track = await bot.wavelink.build_track(track_id)
            em = discord.Embed(title=track.title, description=track.author, color=0x2ECC71)
            em.set_author(name=f"Playing in {channel}")
            em.set_thumbnail(url=track.thumb)
            await cmd.send(embed=em)
            start = dt.now()
            await player.play(track)
            while player.is_playing or player.is_paused:
                await asyncio.sleep(0.5)
            end = dt.now()
            row = await bot.db.conn.fetchrow(f"SELECT * FROM music WHERE id = '{channel.id}';")
            if len(row) == 0:
                queue = []
            else:
                queue = row["queue"]
            if (end - start).seconds < 3:
                await player.disconnect()
                return await cmd.send("It seems that something went wrong with the server. Maybe try it again?") 
        await player.disconnect()


@_play.error
async def play_error(cmd, error):
    if isinstance(cmd, commands.UserInputError):
        await cmd.send(f"Valid argument after `{cmd.prefix}play` is `loop`")
