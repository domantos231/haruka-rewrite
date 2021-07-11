import aiohttp
import asyncio
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from lib.settings import *


session = aiohttp.ClientSession()


class SearchResult:
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


async def get(id):
    url = f"https://myanimelist.net/anime/{id}"
    async with session.get(url) as response:
        if response.status == 200:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            obj = soup.find(name = "h1")
            title = obj.get_text()
            obj = soup.find(name="img", attrs = {"itemprop": "image"})
            image_url = obj.get("data-src")
            try:
                obj = soup.find(name = "span", attrs = {"itemprop": "ratingValue"})
                score = float(obj.get_text())
            except:
                score = None
            try:
                obj = soup.find(name = "span", attrs = {"itemprop": "ratingCount"})
                ranked = int(obj.get_text())
            except:
                ranked = None
            try:
                obj = soup.find(name = "span", attrs = {"class": "numbers popularity"}).strong.extract()
                popularity = int(obj.get_text()[1:])
            except:
                popularity = None
            try:
                obj = soup.find(name = "meta", attrs = {"property": "og:description"})
                synopsis = obj.get("content")
            except:
                synopsis = None
            try:
                obj = soup.find(name="span", string="Type:").parent.a.extract()
                type = obj.get_text()
            except:
                type = None
            try:
                obj = soup.find(name="span", string="Episodes:").parent
                obj.span.extract()
                episodes = int(obj.get_text(strip=True))
            except:
                episodes = None
            try:
                obj = soup.find(name="span", string="Status:").parent
                obj.span.extract()
                status = obj.get_text(strip=True)
            except:
                status = None
            try:
                obj = soup.find(name="span", string="Aired:").parent
                obj.span.extract()
                aired = obj.get_text(strip=True)
            except:
                aired = None
            try:
                obj = soup.find(name="span", string="Broadcast:").parent
                obj.span.extract()
                broadcast = obj.get_text(strip=True)
            except:
                broadcast = None
            genres = []
            try:
                obj = soup.find_all(name="span", attrs = {"itemprop": "genre"})
                for genre in obj:
                    genres.append(genre.get_text())
            except:
                pass
        else:
            await cmd.send("Unable to connect to server")
        return id, title, image_url, score, ranked, popularity, synopsis, type, episodes, status, aired, broadcast, genres, url


@bot.command()
async def anime(cmd, *, query):
    if len(query) < 3:
        await cmd.send(f"Search query must have at least 3 characters")
        return
    rslt = []
    url = f"https://myanimelist.net/anime.php?q={query}"
    async with session.get(url) as response:
        if response.status == 200:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            obj = soup.find_all(name = "a", attrs = {"class": "hoverinfo_trigger fw-b fl-l"}, limit = 6)
            for tag in obj:
                url = tag.get("href")
                id = int(url.split("/")[4])
                title = tag.get_text()
                rslt.append(SearchResult(title, id, url))
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
        id, title, image_url, score, ranked, popularity, synopsis, type, episodes, status, aired, broadcast, genres, url = await get(rslt[choice].id)
        em = discord.Embed(title=title, description=synopsis, color=0x2ECC71)
        em.set_author(name=f"{cmd.author.name}'s request", icon_url=cmd.author.avatar_url)
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
        await cmd.send(embed=em)


@anime.error
async def anime_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again")
