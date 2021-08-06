from settings import *
from discord.ext import commands


@bot.command(name="pause")
@commands.cooldown(1, 5, commands.BucketType.guild)
async def _pause(cmd):
    player = bot.wavelink.get_player(guild_id=cmd.guild.id)
    if player.is_playing:
        await player.set_pause(True)
        await cmd.send("Paused audio.")
    else:
        await cmd.send("No audio currently playing to pause.")