import asyncio
import discord
from settings import *


voice_protocols = {}


@bot.command(name="play")
async def _play(cmd):
    if cmd.author.voice is None:
        await cmd.send("Please join a voice channel first.")
    else:
        channel = cmd.author.voice.channel
        cur.execute("SELECT * FROM queue;")
        lst = cur.fetchall()
        existed = False
        for i in lst:
            if i[0] == str(channel.id):
                existed = True
                queue = i[1]
                break
        if not existed:
            await cmd.send("Please add some songs to the queue first.")
            return
        n = len(queue)
        if n == 0:
            await cmd.send("Please add a song to the queue.")
        elif channel.id in voice_protocols:
            await cmd.send("This voice channel is currently playing.")
        else:
            voice = await channel.connect()
            voice_protocols[channel.id] = voice
            await cmd.send(f"Playing in **{channel}**")
            any = True
            while any:
                audio = discord.FFmpegPCMAudio(f"{root}/music/{channel.id}-music/song1.opus")
                voice.play(audio)
                while voice.is_playing() or voice.is_paused():
                    await asyncio.sleep(0.5)
                cur.execute(f"""
                UPDATE queue
                SET url = url[2:]
                WHERE id = '{channel.id}';
                """)
                conn.commit()
                os.chdir(f"{root}/music/{channel.id}-music")
                try:
                    os.remove("song1.opus")
                except OSError:
                    pass
                any = False
                i = 1
                while os.path.isfile(f"song{i + 1}.opus"):
                    any = True
                    os.rename(f"song{i + 1}.opus", f"song{i}.opus")
                    i += 1
            voice.cleanup()
            await voice.disconnect()
            del voice_protocols[channel.id]


@bot.command(name="pause")
async def _pause(cmd):
    if cmd.author.voice is None:
        await cmd.send("Please join a voice channel first.")
    else:
        channel = cmd.author.voice.channel
        if channel.id in voice_protocols:
            voice = voice_protocols[channel.id]
            if voice.is_playing():
                voice.pause()
                await cmd.send(f"Paused audio in channel **{channel}**")
            else:
                await cmd.send(f"The audio has already been paused! Use {cmd.prefix}resume to resume.")
        else:
            await cmd.send(f"No audio is currently playing in **{channel}**")


@bot.command(name="resume")
async def _resume(cmd):
    if cmd.author.voice is None:
        await cmd.send("Please join a voice channel first.")
    else:
        channel = cmd.author.voice.channel
        if channel.id in voice_protocols:
            voice = voice_protocols[channel.id]
            if voice.is_paused():
                voice.resume()
                await cmd.send(f"Resumed audio in channel **{channel}**")
            else:
                await cmd.send(f"The audio is currently playing, no need to resume.")
        else:
            await cmd.send(f"No audio is currently playing in **{channel}**")
