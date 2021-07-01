from discord.ext import commands
from lib.settings import *


@bot.event
async def on_command_error(cmd, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.CommandOnCooldown):
        await cmd.send(f"<@!{cmd.author.id}> This command is on cooldown!" + " You can use it after **{:.2f}** seconds!".format(error.retry_after))