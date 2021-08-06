from discord.ext import commands
from random import randint
from settings import *


@bot.command(name="roll")
@commands.cooldown(1, 3, commands.BucketType.user)
async def _roll(cmd, *arg):
    if not len(arg) == 2:
        await cmd.send("Please enter 2 integers only!")
    else:
        try:
            i = int(arg[0])
            j = int(arg[1])
            if i < j:
                ans = randint(i, j)
            else:
                ans = randint(j, i)
            await cmd.send(f"<@!{cmd.author.id}> rolled a **{ans}**")
        except:
            await cmd.send("Please enter 2 integers!")
