from settings import *


@bot.event
async def on_wavelink_node_ready(node):
    print(f"HARUKA | Node {node.identifier} is ready.")


@bot.event
async def on_wavelink_track_exception(player, track, error):
    print(f"HARUKA | TrackException in server '{player.guild}' while playing '{track.title}': {error}")
    await player.disconnect(force=True)
