import discord
from discord.ext import commands


# A decorator that only allows TextChannel to invoke a command
def channelCheck():
    async def decorator(cmd):
        if not isinstance(cmd.channel, discord.TextChannel):
            await cmd.send("This command can only be invoked in a server text channel.")
            return False
        return True
    return commands.check(decorator)
