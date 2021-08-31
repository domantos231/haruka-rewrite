import aiohttp
import asyncio
import discord
import gc
from discord.ext import commands
from bs4 import BeautifulSoup
from settings import *
from load import *


@bot.command(
    name = "anime",
    description = "Search for an anime in the MyAnimeList database",
    usage = "anime <query>"
)
@commands.cooldown(1, 6, commands.BucketType.user)
async def _anime(cmd, *, query):
    if len(query) < 3:
        await cmd.send(f"Search query must have at least 3 characters")
        return
    rslt = await bot.search_anime(query)
    if not rslt:
        return await cmd.send("No matching results found.")
    desc = "\n".join(f"{choices[i[0]]} {i[1].title}" for i in enumerate(rslt))
    em = discord.Embed(title=f"Search results for {query}", description=desc, color=0x2ECC71)
    msg = await cmd.send(embed=em)
    for emoji in choices[:len(rslt)]:
        await msg.add_reaction(emoji)
    

    def check(reaction, user):
        return user.id == cmd.author.id and str(reaction) in choices[:len(rslt)] and reaction.message.id == msg.id


    try:
        reaction, user = await bot.wait_for("reaction_add", check=check, timeout=300.0)
    except asyncio.TimeoutError:
        await cmd.send(f"<@!{cmd.author.id}> didn't respond to anime search request. Message timed out.")
        return
    else:
        choice = choices.index(str(reaction))
        id, title, image_url, score, ranked, popularity, synopsis, type, episodes, status, aired, broadcast, genres, url = await bot.get_anime(rslt[choice].id)
        em = discord.Embed(title=title, description=synopsis, color=0x2ECC71)
        em.set_author(name=f"{cmd.author.name}'s request", icon_url=cmd.author.avatar.url)
        em.set_thumbnail(url=image_url)
        em.add_field(name="Genres", value=", ".join(genres), inline=False)
        em.add_field(name="Score", value=score, inline=False)
        em.add_field(name="Aired", value=aired)
        em.add_field(name="Ranked", value=ranked)
        em.add_field(name="Popularity", value=popularity)
        em.add_field(name="Episodes", value=episodes)
        em.add_field(name="Type", value=type)
        em.add_field(name="Broadcast", value=broadcast)
        em.add_field(name="Link reference", value=f"[MyAnimeList link]({url})", inline=False)
        await msg.delete()
        await cmd.send(embed=em)
        del em, id, title, image_url, score, ranked, popularity, synopsis, type, episodes, status, aired, broadcast, genres, url
        gc.collect()
