import discord
import traceback
from discord.ext import commands
from settings import *
from objects import *


async def notify_error(cmd, error):
    try:
        await cmd.send(f"🔧 An error has just occurred, hope it will be fixed soon.")
    except Exception as ex:
        print(f"HARUKA | An exception occurred when trying to send a notification message:")
        traceback.print_tb(ex.__traceback__)
        print(f"HARUKA | {ex}")
    else:
        print("HARUKA | Notification message was successfully sent.")


async def record_error(cmd, error):
    traceback.print_tb(error.__traceback__)
    print(f"HARUKA | '{cmd.message.content}' in {cmd.guild}/{cmd.channel} ({error.__class__.__name__})")
    print(f"HARUKA | {error}")


async def report_error():
    file = discord.File("./log.txt")
    await bot.get_user(ME).send(f"<@!{ME}> An error has just occured. This is the report.", file=file)


@bot.event
async def on_command_error(cmd, error):
    report = False

    if isinstance(error, commands.CommandNotFound):
        """
        Exception raised when a command is attempted to be invoked but no command under that name is found.
        This is not raised for invalid subcommands, rather just the initial main command that is attempted to be invoked.
        """
        pass

    elif isinstance(error, commands.UserInputError):
        """
        The base exception type for errors that involve errors regarding user input.
        """
        await cmd.send("📝 Please check your input again.")

    elif isinstance(error, commands.CommandOnCooldown):
        """
        Exception raised when the command being invoked is on cooldown.
        """
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
    
    # These are the subclasses of commands.CheckFailure
    elif isinstance(error, commands.NotOwner):
        """
        Exception raised when the message author is not the owner of the bot.
        """
        await cmd.send("💻 This command is available for developers only.")
    elif isinstance(error, commands.MissingPermissions):
        """
        Exception raised when the command invoker lacks permissions to run a command.
        """
        await cmd.send("🚫 You do not have the permission to invoke this command.")
    
    elif isinstance(error, discord.Forbidden):
        """
        Exception that’s raised for when status code 403 occurs.
        """
        pass

    elif isinstance(error, commands.CommandInvokeError):
        """
        Exception raised when the command being invoked raised an exception.
        """
        if isinstance(error.original, discord.Forbidden):
            pass
        else:
            await notify_error(cmd, error)
            report = True
    else:
        await notify_error(cmd, error)
        report = True
    
    if report:
        await record_error(cmd, error)
        if isinstance(error, commands.CommandInvokeError):
            print(f"HARUKA | The above exception was caused by the following exception:")
            await record_error(cmd, error.original)
        await report_error()