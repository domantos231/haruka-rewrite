import discord
import gc
from random import choice
from discord.ext import commands
from settings import *


@bot.command(name="cry")
@commands.cooldown(1, 3, commands.BucketType.user)
async def _cry(cmd):
    gifs = await GIF("anime-cry").giphy_leech()
    em = discord.Embed(description=f"**{cmd.author.name}** is crying ~~", color=0x2ECC71)
    em.set_image(url=choice(gifs))
    await cmd.send(embed=em)
    del gifs, em
    gc.collect()