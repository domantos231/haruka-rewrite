import asyncio
import subprocess
import multiprocessing
import sys
from time import sleep


def lavalink_start():
    subprocess.call("java -jar Lavalink.jar", shell=True)


if __name__ == "__main__":
    from settings import *
    from events import *
    from commands import *


    # Run lavalink server
    multiprocessing.set_start_method("spawn")
    p = multiprocessing.Process(target=lavalink_start)
    p.start()
    waiting_time = float(sys.argv[1])
    print(f"HARUKA | Bot will start after {waiting_time} seconds.")
    sleep(waiting_time)
    print("HARUKA | Starting bot...")


    @bot.event
    async def on_connect():
        print("HARUKA | Connected to Discord!")
        if len(bot.db._connection) < 5:
            await bot.db.connect()


    @bot.event
    async def on_ready():
        print(f"HARUKA | Logged in as {bot.user}")


    async def cancel():
        await session.close()
        print("HARUKA | Side session closed.")
        await bot.db.close()


    # Run bot
    try:
        bot.loop.run_until_complete(bot.start(TOKEN))
    except:
        bot.loop.run_until_complete(bot.close())
    finally:
        print("HARUKA | Terminating bot")
        bot.loop.close()
        asyncio.run(cancel())
