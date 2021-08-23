import discord
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
        if seconds < 1800:
            await msg.delete(delay = error.retry_after)
    elif isinstance(error, commands.NotOwner):
        await cmd.send("💻 This command is available for developers only.")
    elif isinstance(error, commands.MissingPermissions):
        await cmd.send("🚫 You do not have the permission to invoke this command.")
    elif isinstance(error, commands.UserInputError):
        await cmd.send("📜 Please check your input again.")
    elif isinstance(error, commands.CommandInvokeError):
        await cmd.send(f"🔧 An error occurred:\n```\n{error.original}\n```\nIf this is a bug, hopefully it will be removed in the future 😉")
        print(f"HARUKA | '{cmd.message.content}' in {cmd.guild}/{cmd.channel} {type(error)} {error}")
    else:
        print(f"HARUKA | '{cmd.message.content}' in {cmd.guild}/{cmd.channel} {type(error)} {error}")
