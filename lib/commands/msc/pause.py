from settings import *


@bot.command(name="pause")
async def _pause(cmd):
    player = bot.wavelink.get_player(guild_id=cmd.guild.id)
    if player.is_playing:
        await player.set_pause(True)
        await cmd.send("Paused audio.")