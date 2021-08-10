import discord
import datetime
from datetime import datetime as dt
from settings import *


@bot.command(name="exec")
async def _exec(cmd, *func):
    if not await bot.is_owner(cmd.author):
        await cmd.send("This command is available for developers only.")
        return
    display = ""
    time = datetime.timedelta(0)
    for f in func:
        if f.startswith("await"):
            try:
                start = dt.now()
                await eval(f[6:])
                end = dt.now()
                time += end - start
            except Exception as ex:
                display += f"Exception at '{f}': {ex}\n"
        else:
            try:
                start = dt.now()
                exec(f)
                end = dt.now()
                time += end - start
            except Exception as ex:
                display += f"Exception at '{f}': {ex}\n"
    if len(display) > 0:
        await cmd.send(display)
    else:
        await cmd.send(f"Process executed in {time} seconds.")