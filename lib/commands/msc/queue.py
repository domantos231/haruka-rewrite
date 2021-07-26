import aiohttp
import asyncio
import configparser
import discord
import os
import platform
import re
from discord.ext import commands
from lib.settings import *


class BusyQueueError(Exception):
    pass


EmptyArray = r"{}"


@bot.command(name="queue")
async def _queue(cmd, url = None):
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
                desc = "\n".join(f"**#{obj[0] + 1}** {obj[1]}" for obj in enumerate(queue))
                break
        if not existed:
            queue = []
            cur.execute(f"""
            INSERT INTO queue
            VALUES ('{channel.id}', '{EmptyArray}');
            """)
            conn.commit()
        n = len(queue)
        if n == 0:
            desc = f"Add some songs to the queue.\nEg: `{cmd.prefix}queue <YouTube URL>`"
        em = discord.Embed(title=f"Music queue in channel {channel}", description=desc, color=0x2ECC71)
        if url is not None:
            if ";" in url or re.match(r"^((https://|http://)?(www.)?(youtube.com|youtu.be))", url) is None:
                await cmd.send("It seems like your URL is invalid. Maybe check it again?")
            else:
                config = configparser.ConfigParser()
                try:
                    os.chdir(f"{root}/music/{channel.id}-music")
                    config.read("config.ini")
                    if config["general"]["status"] == "busy":
                        raise BusyQueueError
                except OSError:
                    os.mkdir(f"{root}/music/{channel.id}-music")
                    os.chdir(f"{root}/music/{channel.id}-music")
                    config["general"] = {"status": "busy"}
                    with open("config.ini", "w") as inifile:
                        config.write(inifile)
                except BusyQueueError:
                    await cmd.send("This voice channel queue is currently busy.")
                    return
                config["general"] = {"status": "busy"}
                with open("config.ini", "w") as inifile:
                    config.write(inifile)
                msg = await cmd.send("Processing queue...")
                if platform.system() == "Windows":
                    process = await asyncio.create_subprocess_shell(f"youtube-dl --no-playlist --extract-audio --audio-format \"opus\" --match-filter \"!is_live\" --force-ipv4 --rm-cache-dir -o \"song{n + 1}.%(ext)s\" {url}")
                else:
                    process = await asyncio.create_subprocess_shell(f"youtube-dl --no-playlist --extract-audio --audio-format 'opus' --match-filter '!is_live' --force-ipv4 --rm-cache-dir -o 'song{n + 1}.%(ext)s\' {url}")
                code = await process.wait()
                config["general"] = {"status": "ready"}
                with open("config.ini", "w") as inifile:
                    config.write(inifile)
                await msg.delete()
                if os.path.isfile(f"./song{n + 1}.opus"):
                    os.chdir(root)
                    cur.execute(f"""
                    UPDATE queue
                    SET url = array_append(url, '{url}')
                    WHERE id = '{channel.id}';
                    """)
                    conn.commit()
                    add_em = discord.Embed(title=f"Channel **{channel}**", description=url, color=0x2ECC71)
                    add_em.set_author(name=f"{cmd.author.name} added 1 song to queue", icon_url=cmd.author.avatar_url)
                    await cmd.send(embed=add_em)
                else:
                    os.chdir(root)
                    await cmd.send("It seems like your URL is invalid. Maybe check it again?\nNote that live audios cannot be added to queue.")
        else:
            em.set_footer(text=f"Currently has {n} song(s)")
            await cmd.send(embed=em)


@_queue.error
async def queue_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please enter a valid YouTube URL.")