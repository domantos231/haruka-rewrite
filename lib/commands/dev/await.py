from settings import *


@bot.command(name="await")
async def _await(cmd, *, coro):
    if not await bot.is_owner(cmd.author):
        await cmd.send("This command is available for developers only.")
        return
    try:
        await eval(coro)
    except Exception as ex:
        await cmd.send(ex)
