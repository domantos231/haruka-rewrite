import discord
from settings import *


@bot.command(name="exec")
async def _exec(cmd, *func):
    if not await bot.is_owner(cmd.author):
        await cmd.send("This command is available for developers only.")
        return
    display = ""
    for f in func:
        if f.startswith("await"):
            try:
                await eval(f[6:])
            except Exception as ex:
                display += f"Exception at {f}: {ex}\n"
        else:
            try:
                eval(f)
            except Exception as ex:
                display += f"Exception at {f}: {ex}\n"
    await cmd.send(display)