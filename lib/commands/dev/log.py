import discord
from discord.ext import commands
from settings import *


@bot.command(
    name = "log",
    description = "Send the log file",
)
@commands.is_owner()
async def _log(cmd):
    await cmd.send(content="This is the log file", file=discord.File("./log.txt"))
