import asyncio


if __name__ == "__main__":
    from settings import *
    from events import *
    from commands import *


    @bot.event
    async def on_connect():
        print("HARUKA | Connected to Discord!")


    @bot.event
    async def on_ready():
        print(f"HARUKA | Logged in as {bot.user} | Running in {len(bot.guilds)} servers.")


    async def cancel():
        await bot.db.close()


    # Run bot
    try:
        bot.loop.run_until_complete(bot.start(TOKEN))
    except Exception as ex:
        print(f"HARUKA | An exception occured: {ex}")
        bot.loop.run_until_complete(bot.close())
    finally:
        print("HARUKA | Terminating bot")
        bot.loop.close()
        asyncio.run(cancel())
