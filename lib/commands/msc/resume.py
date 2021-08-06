from settings import *
from discord.ext import commands


@bot.command(name="resume")
@commands.cooldown(1, 5, commands.BucketType.guild)
async def _resume(cmd):
    player = bot.wavelink.get_player(guild_id=cmd.guild.id)
    if player.is_paused:
        await player.set_pause(False)
        await cmd.send("Resumed audio.")
    else:
        await cmd.send("No audio currently being paused to resume.")