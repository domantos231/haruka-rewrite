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
        em = result.create_embed()
        em.set_author(
            name = f"{cmd.author.name} searched for {query}",
            icon_url = cmd.author.avatar.url if cmd.author.avatar else None,
        )
        await cmd.send(embed=em)
    else:
        await cmd.send("No matching result was found.")
