import discord
import os
import random
from PIL import Image
from discord.ext import commands
from settings import *


_card_limit = 9


@bot.command(name="card")
@commands.cooldown(1, 10, commands.BucketType.user)
async def _card(cmd, n: int = 1):
    if n < 1 or n > _card_limit:
        return await cmd.send(f"Invalid card number (must be from 1 to {_card_limit}).")
    ignore = []
    cards = []
    for i in range(n):
        card = PlayingCard.draw(ignore)
        ignore.append(card.filename)
        cards.append(card)
    PlayingHand(cards).image.save(f"./lib/assets/cards/{cmd.message.id}.png")
    file = discord.File(f"./lib/assets/cards/{cmd.message.id}.png", filename = "image.png")
    embed = discord.Embed(title=f"{cmd.author.name} drew {n} card(s)!", color=0x2ECC71)
    embed.set_image(url="attachment://image.png")
    await cmd.send(file=file, embed=embed)
    os.remove(f"./lib/assets/cards/{cmd.message.id}.png")
