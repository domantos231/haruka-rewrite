import discord
import gc
from random import choice
from discord.ext import commands
from settings import *


@bot.command(
    name = "girl",
    description = "Get you a 2D girl",
)
@commands.cooldown(1, 6, commands.BucketType.user)
async def _girl(cmd):
    gifs = await bot.giphy("anime-girl")
    em = discord.Embed(description=f"**{cmd.author.name}**, this is your girl!", color=0x2ECC71)
    em.set_image(url=choice(gifs))
    await cmd.send(embed=em)
    del gifs, em
    gc.collect()