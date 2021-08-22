from discord.ext import commands
from datetime import datetime as dt
from settings import *


@bot.command(name="sql")
async def _sql(cmd, *, query):
    if not await bot.is_owner(cmd.author):
        return await cmd.send("This command is available for developers only.")
    try:
        start = dt.now()
        await bot.db.conn.execute(query)
        end = dt.now()
    except Exception as ex:
        await cmd.send(f"An exception occured: {ex}")
    else:
        await cmd.send(f"Process executed in {end - start}")
