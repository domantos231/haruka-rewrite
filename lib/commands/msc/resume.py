from settings import *


@bot.command(name="resume")
async def _resume(cmd):
    player = bot.wavelink.get_player(guild_id=cmd.guild.id)
    if player.is_paused:
        await player.set_pause(False)
        await cmd.send("Resumed audio.")
    else:
        await cmd.send("No audio currently being paused to resume.")