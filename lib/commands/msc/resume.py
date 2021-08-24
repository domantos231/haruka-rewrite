from settings import *
from discord.ext import commands


@bot.command(
    name = "resume",
    description = "Resume the paused audio"
)
@commands.cooldown(1, 5, commands.BucketType.guild)
async def _resume(cmd):
    player = bot.node.get_player(cmd.guild)
    if player and player.is_paused:
        await player.resume()
        await cmd.send("Resumed audio.")
    else:
        await cmd.send("No audio currently being paused to resume.")