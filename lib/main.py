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
    print(f"Bot will start after {waiting_time} seconds.")
    sleep(waiting_time)
    print("Starting bot...")


    @bot.event
    async def on_connect():
        print("Connected to Discord!")


    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")
        if len(bot.db._connection) == 0:
            await bot.db.connect()


    async def cancel():
        await session.close()
        print("Side session closed.")
        await bot.db.close()
        print("Closed all database connections.")


    # Run bot
    try:
        bot.loop.run_until_complete(bot.start(TOKEN))
    except:
        bot.loop.run_until_complete(bot.close())
    finally:
        asyncio.run(cancel())
        bot.loop.close()
