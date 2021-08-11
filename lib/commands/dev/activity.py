import discord
from discord.ext import commands
from settings import *


@bot.group(name="activity", case_insensitive=True)
@commands.is_owner()
async def _activity(cmd):
    pass


@_activity.command(name="watching")
async def _watching(cmd, *, desc):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=desc))


@_activity.command(name="playing")
async def _playing(cmd, *, desc):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=desc))


@_activity.command(name="listening")
async def _listening(cmd, *, desc):
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=desc))


@_activity.error
async def activity_error(cmd, error):
    if isinstance(error, commands.NotOwner):
        await cmd.send("This command is available for developers only.")
    elif isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again")