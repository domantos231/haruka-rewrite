import discord
from settings import *


@bot.command(name="log")
async def _log(cmd):
    if not await bot.is_owner(cmd.author):
        return await cmd.send("This command is available for developers only.")
    await cmd.send(content="This is the log file", file=discord.File("./log.txt"))
