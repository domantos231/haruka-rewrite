import discord
import traceback
from discord.ext import commands
from settings import *
from objects import *


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
        await cmd.send("📝 Please check your input again.")
    elif isinstance(error, MyAnimeListException):
        await cmd.send("🌎 Cannot connect to MyAnimeList.")
    else:
        traceback.print_tb(error.__traceback__)
        print(f"HARUKA | '{cmd.message.content}' in {cmd.guild}/{cmd.channel} ({error.__class__.__name__})")
        print(f"HARUKA | {error}")
        try:
            await cmd.send(f"🔧 An error occurred:\n```\n{error.original}\n```")
        except Exception as ex:
            print(f"HARUKA | Another exception occurred when trying to send a notification message:")
            traceback.print_tb(ex.__traceback__)
            print(f"HARUKA | {ex}")
        else:
            print("HARUKA | Notification message was successfully sent.")
        file = discord.File("./log.txt")
        await bot.get_user(ME).send(f"<@!{ME}> An error has just occured in `{cmd.guild}/{cmd.channel}`. This is the report.", file=file)
