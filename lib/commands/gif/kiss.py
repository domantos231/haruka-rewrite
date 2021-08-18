import discord
import gc
from random import choice
from discord.ext import commands
from settings import *


@bot.command(name="kiss")
@commands.cooldown(1, 3, commands.BucketType.user)
async def _kiss(cmd, user: discord.User = None):
    if user is None:
        await cmd.send(f"Who do you want to kiss, {cmd.author.name}?")
    elif user.id == cmd.author.id:
        await cmd.send("Are you kissing a mirror?")
    else:
        gifs = await bot.giphy("anime-kiss")
        em = discord.Embed(description=f"**{cmd.author.name}** kissed **{user.name}** 💞💞", color=0x2ECC71)
        em.set_image(url=choice(gifs))
        await cmd.send(embed=em)
        del gifs, em
        gc.collect()


@_kiss.error
async def kiss_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")