import discord
import gc
from random import choice
from discord.ext import commands
from settings import *


@bot.command(
    name = "cry",
    description = "Burst in tear?",
)
@commands.cooldown(1, 6, commands.BucketType.user)
async def _cry(cmd):
    gifs = await bot.giphy("anime-cry")
    em = discord.Embed(description=f"**{cmd.author.name}** is crying ~~", color=0x2ECC71)
    em.set_image(url=choice(gifs))
    await cmd.send(embed=em)
    del gifs, em
    gc.collect()