from settings import *


@bot.command(name="stop")
@commands.cooldown(1, 5, commands.BucketType.guild)
async def _stop(cmd):
    player = bot.wavelink.get_player(guild_id=cmd.guild.id)
    if player.is_connected:
        await player.destroy()
        await cmd.send("Stopped player.")
    else:
        await cmd.send("No currently connected player.")