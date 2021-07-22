import asyncio
from lib.settings import bot, TOKEN, session
from lib import *


async def cancel(session):
    await session.close()
    print("Side session closed.")


try:
    bot.loop.run_until_complete(bot.start(TOKEN))
except:
    bot.loop.run_until_complete(bot.close())
finally:
    bot.loop.close()
    asyncio.run(cancel(session))
