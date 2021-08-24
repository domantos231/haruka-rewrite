import discord
from discord.ext import commands
from settings import *


@bot.group(
    name = "activity",
    description = "Change bot activity",
    usage = "activity <watching/playing/listening> <description>",
)
@commands.is_owner()
async def _activity(cmd):
    pass


@_activity.command(name="watching")
async def _watching(cmd, *, desc):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=desc))
    await cmd.send("Success")


@_activity.command(name="playing")
async def _playing(cmd, *, desc):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=desc))
    await cmd.send("Success")


@_activity.command(name="listening")
async def _listening(cmd, *, desc):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=desc))
    await cmd.send("Success")
