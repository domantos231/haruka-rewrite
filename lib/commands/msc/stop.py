from settings import *


@bot.command(name="stop")
async def _stop(cmd):
    player = await bot.wavelink.get_player(guild_id=cmd.guild.id)
    if player.is_connected:
        await player.destroy()
        await cmd.send("Stopped player.")