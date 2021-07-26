import aiohttp
import asyncio
import discord
from discord.ext import commands
from bs4 import BeautifulSoup as bs
from lib.settings import *


class UrbanSearch:
    def __init__(self, title, meaning, example, url):
        self._title = title
        self._meaning = meaning
        self._example = example
        self._url = url
        
        
    @property
    def title(self):
        return self._title


    @property
    def meaning(self):
        return self._meaning


    @property
    def example(self):
        return self._example


    @property
    def url(self):
        return self._url


async def main(word):
    url = f"https://www.urbandictionary.com/define.php?term={word}"
    async with session.get(url) as response:
        if response.status == 200:
            html = await response.text()
            html = html.replace("<br/>", "\n").replace("\r", "\n")
            soup = bs(html, "html.parser")
            obj = soup.find(name="div", attrs={"class": "def-header"})
            title = obj.get_text()
            try:
                obj = soup.find(name="div", attrs={"class": "meaning"})
                meaning = "\n".join(i for i in obj.get_text().split("\n") if len(i) > 0)
            except:
                meaning = None
            try:
                obj = soup.find(name="div", attrs={"class": "example"})
                example = "\n".join(i for i in obj.get_text().split("\n") if len(i) > 0)
            except:
                example = None
            return UrbanSearch(title, meaning, example, url)
        else:
            return None


@bot.command(name="search")
async def _search(cmd, *, query):
    result = await main(query)
    if result is not None:
        desc = f"{result.meaning}\n---------------\n{result.example}"
        em = discord.Embed(title=f"{result.title}", description=desc, color=0x2ECC71)
        em.set_author(name=f"{cmd.author.name} searched for {query}", icon_url=cmd.author.avatar_url)
        em.set_footer(text="From Urban Dictionary")
        await cmd.send(embed=em)
    else:
        await cmd.send("No matching result was found.")


@_search.error
async def search_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again")
