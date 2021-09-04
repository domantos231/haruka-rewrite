import discord
import gc
from random import choice
from discord.ext import commands
from settings import *


@bot.command(
    name = "loli",
    description = "Get you a 2D loli but be aware of the FBI",
)
@commands.cooldown(1, 6, commands.BucketType.user)
async def _loli(cmd):
    loli = await bot.gif("anime-loli")
    fbi = await bot.gif("fbi")
    url = choice([*loli, *fbi])
    if url in loli:
        em = discord.Embed(description=f"**{cmd.author.name}**, this is your loli!", color=0x2ECC71)
    else:
        em = discord.Embed(description=f"**{cmd.author.name}** was arrested.", color=0x2ECC71)
    em.set_image(url=url)
    await cmd.send(embed=em)
    del loli, fbi, em
    gc.collect()