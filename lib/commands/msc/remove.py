import asyncio
import configparser
import discord
import os
import platform
from discord.ext import commands
from settings import *


@bot.command(name="remove")
async def _remove(cmd, n: int):
    if cmd.author.voice is None:
        await cmd.send("Please join a voice channel first.")
    else:
        channel = cmd.author.voice.channel
        config = configparser.ConfigParser()
        try:
            config.read(f"{root}/music/{channel.id}-music/config.ini")
        except:
            await cmd.send("This channel has not added any songs to queue.")
            return
        else:
            if config["general"]["status"] == "busy":
                await cmd.send("This voice channel queue is currently busy.")
                return
        if platform.system() == "Windows":
            command = f"del /f \"{root}\music\\{channel.id}-music\\song{n}.opus\""
            process = await asyncio.create_subprocess_shell(command)
        else:
            process = await asyncio.create_subprocess_shell(f"rm -f '{root}/music/{channel.id}-music/song{n}.opus'")
        code = await process.wait()
        if code == 0:
            i = n
            while os.path.isfile(f"{root}/music/{channel.id}-music/song{i+1}.opus"):
                os.rename(f"{root}/music/{channel.id}-music/song{i+1}.opus", f"{root}/music/{channel.id}-music/song{i}.opus")
                i += 1
            cur.execute(f"""
            UPDATE queue
            SET url = array_cat(url[:{n - 1}], url[{n + 1}:])
            WHERE id = '{channel.id}';
            """)
            conn.commit()
            await cmd.send(f"Successfully removed **#{n}**")
        else:
            await cmd.send("An error has occured, cannot remove song.")


@_remove.error
async def remove_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")
