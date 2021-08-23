from discord.ext import commands
from random import randint
from settings import *


@bot.command(name="8ball")
@commands.cooldown(1, 6, commands.BucketType.user)
async def _8ball(cmd, *, arg):
    if arg.lower().startswith(("what", "which", "why", "when", "how", "where", "who")):
        await cmd.send("Please ask another question.")
    elif (
        arg.lower().startswith(
            (
                "do",
                "does",
                "am",
                "is",
                "are",
                "can",
                "could",
                "would",
                "may",
                "should",
                "will",
                "were",
                "was",
            )
        )
        or arg.lower().endswith("?")
    ):
        ans = randint(-4, 4)
        if ans == -4:
            await cmd.send("Don't count on it.")
        if ans == -3:
            await cmd.send("No.")
        if ans == -2:
            await cmd.send("Certainly not.")
        if ans == -1:
            await cmd.send("My source says no.")
        if ans == 0:
            await cmd.send("Better not tell you now.")
        if ans == 1:
            await cmd.send("It is certain.")
        if ans == 2:
            await cmd.send("Without a doubt.")
        if ans == 3:
            await cmd.send("Yes.")
        if ans == 4:
            await cmd.send("Most likely.")
    else:
        await cmd.send("Concentrate and ask again.")
