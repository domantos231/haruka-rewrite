import discord
from random import choice
from discord.ext import commands
from settings import *


@bot.command(name="hug")
async def _hug(cmd, user: discord.User = None):
    if user is None:
        await cmd.send(f"Who do you want to hug, {cmd.author.name}?")
    elif user.id == cmd.author.id:
        await cmd.send("Imagine hugging yourself...")
    else:
        gifs = await GIF("anime-hug").giphy_leech()
        em = discord.Embed(description=f"**{cmd.author.name}** gave **{user.name}** a warming hug!", color=0x2ECC71)
        em.set_image(url=choice(gifs))
        await cmd.send(embed=em)


@_hug.error
async def hug_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")