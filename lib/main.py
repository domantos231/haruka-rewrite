import asyncio
import subprocess
import multiprocessing
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
    waiting_time = 10.0
    print(f"Bot will start after {waiting_time} seconds.")
    sleep(waiting_time)
    print("Starting bot...")


    @bot.event
    async def on_connect():
        print("Connected to Discord!")


    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")
        try:
            bot.db._connection
        except AttributeError:
            await bot.db.connect()


    async def cancel():
        await session.close()
        print("Side session closed.")


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
