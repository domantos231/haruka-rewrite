import asyncio
import multiprocessing
import os
import platform
import shutil
import subprocess
import sys
from configparser import ConfigParser


# Load music queue from a voice channel
config = ConfigParser()
config["general"] = {"status": "ready"}
root_ = os.getcwd()
def queue_load(id, queue):
    channel_path = f"{root_}/music/{id}-music"
    try:
        shutil.rmtree(f"{root_}/music/{id}-music")
    except:
        pass
    finally:
        os.mkdir(f"{channel_path}")
        os.chdir(f"{channel_path}")
        with open("config.ini", "w") as inifile:
            config.write(inifile)
        for link in enumerate(queue):
            if platform.system() == "Windows":
                subprocess.call(f"youtube-dl --no-playlist --extract-audio --audio-format \"opus\" --match-filter \"!is_live\" --force-ipv4 --rm-cache-dir -o \"{channel_path}\\song{link[0] + 1}.%(ext)s\" {link[1]}", shell = True)
            else:
                subprocess.call(f"youtube-dl --no-playlist --extract-audio --audio-format 'opus' --match-filter '!is_live' --force-ipv4 --rm-cache-dir -o '{channel_path}/song{link[0] + 1}.%(ext)s' {link[1]}", shell = True)


if __name__ == "__main__":
    from settings import *
    from events import *
    from commands import *


    @bot.event
    async def on_connect():
        print("Connected to Discord!")


    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")


    async def cancel():
        await session.close()
        print("Side session closed.")


    # Initialize all music queue if not in debug mode
    if len(sys.argv) == 1:
        multiprocessing.set_start_method("spawn")
        cur.execute("SELECT * FROM queue;")
        lst = cur.fetchall()
        processes = []
        for obj in lst:
            p = multiprocessing.Process(target=queue_load, args=obj)
            p.start()
            processes.append(p)
            if len(processes) == max_processes:
                for process in processes:
                    process.join()
                processes = []
        for process in processes:
            process.join()
    elif sys.argv[1] == "debug":
        print("Running in debug mode... Skipped music queue initialization")
    else:
        sys.exit("Unknown option")


    # Run bot
    try:
        bot.loop.run_until_complete(bot.start(TOKEN))
    except:
        bot.loop.run_until_complete(bot.close())
    finally:
        bot.loop.close()
        asyncio.run(cancel())
        cur.close()
        conn.close()
