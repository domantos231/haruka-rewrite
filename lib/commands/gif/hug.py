import discord
import gc
from random import choice
from discord.ext import commands
from settings import *


@bot.command(name="hug")
@commands.cooldown(1, 6, commands.BucketType.user)
async def _hug(cmd, user: discord.User = None):
    if user is None:
        await cmd.send(f"Who do you want to hug, {cmd.author.name}?")
    elif user.id == cmd.author.id:
        await cmd.send("Imagine hugging yourself...")
    else:
        gifs = await bot.giphy("anime-hug")
        em = discord.Embed(description=f"**{cmd.author.name}** gave **{user.name}** a warming hug!", color=0x2ECC71)
        em.set_image(url=choice(gifs))
        await cmd.send(embed=em)
        del gifs, em
        gc.collect()
