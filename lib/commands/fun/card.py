import discord
import os
import random
from PIL import Image
from discord.ext import commands
from settings import *


cardlist = [f for f in os.listdir(assets_dir)]


@bot.command(name="card")
@commands.cooldown(1, 6, commands.BucketType.user)
async def _card(cmd, n: int = 1):
    if n < 1 or n > 6:
        return await cmd.send("Invalid card number (must be from 1 to 6).")
    lst = []
    empty = Image.new("RGBA", (80 * n, 100))
    for i in range(n):
        f = random.choice(cardlist)
        img = Image.open(f"{assets_dir}/{f}")
        empty.paste(img, (80 * i, 0, 80 * i + 80, 100))
    empty.save(f"{assets_dir}/{cmd.message.id}.png")
    file = discord.File(f"{assets_dir}/{cmd.message.id}.png", filename = "image.png")
    embed = discord.Embed(title=f"{cmd.author.name} drew {n} card(s)!", color=0x2ECC71)
    embed.set_image(url="attachment://image.png")
    await cmd.send(file=file, embed=embed)
    os.remove(f"{assets_dir}/{cmd.message.id}.png")


@_card.error
async def card_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")
    else:
        print(f"HARUKA | '{cmd.message.content}': {error}")