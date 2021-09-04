from settings import *


@bot.command(
    name = "stop",
    description = "Stop the playing audio and disconnect from the voice channel"
)
@commands.cooldown(1, 5, commands.BucketType.guild)
async def _stop(cmd):
    player = bot.node.get_player(cmd.guild)
    if player and player.is_connected:
        await player.stop()
        await player.disconnect(force=True)
        await cmd.send("Stopped player.")
    else:
        await cmd.send("No currently connected player.")