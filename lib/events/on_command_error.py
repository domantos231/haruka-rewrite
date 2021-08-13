from discord.ext import commands
from settings import *


@bot.event
async def on_command_error(cmd, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.CommandOnCooldown):
        seconds = error.retry_after
        days = int(seconds / 86400)
        seconds -= days * 86400
        hours = int(seconds / 3600)
        seconds -= hours * 3600
        minutes = int(seconds / 60)
        seconds -= minutes * 60
        time = ""
        if days > 0:
            time += f" {days}d"
        if hours > 0:
            time += f" {hours}h"
        if minutes > 0:
            time += f" {minutes}m"
        if seconds > 0:
            time += " {:.2f}s".format(seconds)
        msg = await cmd.send(f"⏱️ <@!{cmd.author.id}> This command is on cooldown!\nYou can use it after**{time}**!")
        await msg.delete(delay = error.retry_after)
    elif hasattr(cmd.command, "on_error"):
        pass
    else:
        print(f"['{cmd.message.content}'] {error}")
