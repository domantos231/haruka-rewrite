import aiohttp
import asyncio
import discord
from discord.ext import commands
from settings import *


@bot.command(
    name = "urban",
    description = "Search for a term from Urban Dictionary",
    usage = "urban <query>"
)
@commands.cooldown(1, 6, commands.BucketType.user)
async def _urban(cmd, *, query):
    result = await bot.search_urban(query)
    if result is not None:
        desc = f"{result.meaning}\n---------------\n{result.example}"
        desc.replace("*", r"\*")
        if len(desc) > 4096:
            desc = desc[:4090] + " [...]"
        em = discord.Embed(
            title = f"{result.title}",
            description = desc,
            url = result.url,
            color = 0x2ECC71,
        )
        em.set_author(name=f"{cmd.author.name} searched for {query}", icon_url=cmd.author.avatar.url)
        em.set_footer(text="From Urban Dictionary")
        await cmd.send(embed=em)
    else:
        await cmd.send("No matching result was found.")
