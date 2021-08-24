from discord.ext import commands
from datetime import datetime as dt
from settings import *


@bot.command(
    name = "sql",
    description = "Perform a SQL query",
    usage = "sql <query>",
)
@commands.is_owner()
async def _sql(cmd, *, query):
    try:
        start = dt.now()
        await bot.db.conn.execute(query)
        end = dt.now()
    except Exception as ex:
        await cmd.send(f"An exception occured: {ex}")
    else:
        await cmd.send(f"Process executed in {end - start}")
