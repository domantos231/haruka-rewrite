import discord
import gc
from random import choice
from discord.ext import commands
from settings import *


@bot.command(
    name = "punch",
    description = "Punch someone",
    usage = "punch <user>",
)
@commands.cooldown(1, 6, commands.BucketType.user)
async def _punch(cmd, user: discord.User = None):
    if user is None:
        await cmd.send(f"Who do you want to punch, {cmd.author.name}?")
    elif user.id == cmd.author.id:
        await cmd.send(f"Please don't punch yourself, {cmd.author.name}?")
    else:
        gifs = await bot.giphy("punch")
        em = discord.Embed(description=f"**{cmd.author.name}** punched **{user.name}**!", color=0x2ECC71)
        em.set_image(url=choice(gifs))
        await cmd.send(embed=em)
        del gifs, em
        gc.collect()
