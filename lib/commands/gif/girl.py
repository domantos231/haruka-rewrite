import discord
from random import choice
from discord.ext import commands
from settings import *


@bot.command(name="girl")
async def _girl(cmd):
    gifs = await GIF("anime-girl").giphy_leech()
    em = discord.Embed(description=f"**{cmd.author.name}**, this is your girl!", color=0x2ECC71)
    em.set_image(url=choice(gifs))
    await cmd.send(embed=em)
