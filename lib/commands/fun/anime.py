import aiohttp
import asyncio
import discord
import gc
from discord.ext import commands
from bs4 import BeautifulSoup
from settings import *


class AnimeSearchResult:
    def __init__(self, title, id, url):
        self._title = title
        self._id = id
        self._url = url


    @property
    def title(self):
        return self._title


    @property
    def id(self):
        return self._id


    @property
    def url(self):
        return self._url


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
    rslt = []
    url = f"https://myanimelist.net/anime.php?q={query}"
    async with bot.session.get(url) as response:
        if response.status == 200:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            obj = soup.find_all(name = "a", attrs = {"class": "hoverinfo_trigger fw-b fl-l"}, limit = 6)
            for tag in obj:
                url = tag.get("href")
                id = int(url.split("/")[4])
                title = tag.get_text()
                rslt.append(AnimeSearchResult(title, id, url))
    n = len(rslt)
    desc = "\n".join(f"**#{i+1}** {rslt[i].title}" for i in range(n))
    em = discord.Embed(title=f"Search results for {query}", description=desc, color=0x2ECC71)
    msg = await cmd.send(embed=em)
    for emoji in choices[:n]:
        await msg.add_reaction(emoji)
    

    def check(reaction, user):
        return user.id == cmd.author.id and str(reaction) in choices[:n] and reaction.message.id == msg.id


    try:
        reaction, user = await bot.wait_for("reaction_add", check=check, timeout=300.0)
    except asyncio.TimeOutError:
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
