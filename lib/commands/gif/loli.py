import discord
import gc
from random import choice
from discord.ext import commands
from settings import *


@bot.command(name="loli")
@commands.cooldown(1, 3, commands.BucketType.user)
async def _loli(cmd):
    loli = await GIF("anime-loli").giphy_leech()
    fbi = await GIF("fbi").giphy_leech()
    url = choice([*loli, *fbi])
    if url in loli:
        em = discord.Embed(description=f"**{cmd.author.name}**, this is your loli!", color=0x2ECC71)
    else:
        em = discord.Embed(description=f"**{cmd.author.name}** was arrested.", color=0x2ECC71)
    em.set_image(url=url)
    await cmd.send(embed=em)
    del loli, fbi, em
    gc.collect()