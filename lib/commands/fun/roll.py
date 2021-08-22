from discord.ext import commands
from random import randint
from settings import *


@bot.command(name="roll")
@commands.cooldown(1, 6, commands.BucketType.user)
async def _roll(cmd, i: int, j: int):
    if i < j:
        ans = randint(i, j)
    else:
        ans = randint(j, i)
    await cmd.send(f"<@!{cmd.author.id}> rolled a(n) **{ans}**")
