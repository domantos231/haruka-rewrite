from settings import *


@bot.command(name="play")
async def _play(cmd):
    if not cmd.author.voice:
        await cmd.send("Please join a voice channel first.")
    else:
        channel = cmd.author.voice.channel
        if queue[channel.id].empty():
            return await cmd.send("Please add at least one song to the queue.")
        player = bot.wavelink.get_player(guild_id=cmd.guild.id)
        if not player.channel_id:
            await player.connect(channel.id)
            await cmd.send(f"Connected to **{channel}**")
        elif not player.channel_id == channel.id:
            return await cmd.send(f"I'm currently playing in another voice channel! Consider using `{cmd.prefix}stop`.")
        while not queue[channel.id].empty():
            track = await queue[channel.id].get()
            await player.play(track)
        await player.disconnect()
