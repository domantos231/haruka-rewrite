import discord
import multiprocessing
import subprocess
import sys
import time


def lavalink():
    subprocess.call("java -jar Lavalink.jar", shell = True)


if __name__ == "__main__":
    from settings import *
    from events import *
    from commands import *


    # Run lavalink server
    multiprocessing.set_start_method("spawn")
    proc = multiprocessing.Process(target = lavalink)
    proc.start()
    waiting_time = float(sys.argv[2])
    print(f"HARUKA | Bot will start after {waiting_time} seconds.")
    time.sleep(waiting_time)
    print("HARUKA | Starting bot...")


    @bot.event
    async def on_connect():
        print("HARUKA | Connected to Discord!")


    @bot.event
    async def on_ready():
        file = discord.File("./log.txt")
        await bot.get_user(ME).send(f"<@!{ME}> Bot has just started. This is the report.", file = file)
        print(f"HARUKA | Logged in as {bot.user} | Running in {len(bot.guilds)} servers.")


    # Run the bot
    bot.run(TOKEN)