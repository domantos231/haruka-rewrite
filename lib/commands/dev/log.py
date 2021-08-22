import discord
from discord.ext import commands
from settings import *


@bot.command(name="log")
@commands.is_owner()
async def _log(cmd):
    await cmd.send(content="This is the log file", file=discord.File("./log.txt"))
