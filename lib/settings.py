import asyncio
import asyncpg
import aiohttp
import discord
import gc
import logging
import os
import re
import sys
from io import BytesIO
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
from discord.ext import tasks, commands
from typing import *
from load import *


# Set up logging and garbage collector
if len(sys.argv) == 1:
    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.INFO)
    discord_logger.addHandler(logging.FileHandler(filename="log.txt", mode="a"))
elif sys.argv[1] == "debug":
    logging.basicConfig(level=logging.INFO)
gc.enable()


# Initialize root path and side session
TOKEN = os.environ["TOKEN"]
DATABASE_URL = os.environ["DATABASE_URL"]
API_KEY = os.environ["API_KEY"]
session = aiohttp.ClientSession()
root = os.getcwd()


# Define frequently used emoji lists
checker = ["❌", "✔️"]
choices = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
navigate = ["⬅️", "➡️"]


# Define YouTube API and Invidious URLs
youtube_api_url = "https://www.googleapis.com/youtube/v3"
invidious_urls = [
    "https://invidious-jp.kavin.rocks",
    "https://invidio.xamh.de",
    "https://invidious.exonip.de",
    "https://invidious.silkky.cloud",
    "https://youtube.076.ne.jp",
    "https://invidious.namazso.eu",
    "https://invidious.snopyta.org",
    "https://ytb.trom.tf",
    "https://vid.puffyan.us",
    "https://invidious.hub.ne.kr",
    "https://yewtu.be",
    "https://invidious.kavin.rocks",
    "https://ytprivate.com",
    "https://invidious.noho.st",
    "https://inv.riverside.rocks",
]


# Define giphy image URL RegEx
giphy_pattern_regex = r'(?=(http://|https://))[^"|?]+giphy[.]gif'


# Load economy data from database
class data:
    def __init__(self, id):
        self.id = id
    

    @property
    async def player(self):
        row = await bot.db.conn.fetchrow(f"SELECT * FROM economy WHERE id = '{self.id}';")
        if not row:
            return None
        amt = row["amt"]
        time = row["time"]
        bank = row["bank"]
        interest = row["interest"]
        pet = []
        for obj in enumerate(row["pet"]):
            pet.append(add_pet_data(obj[0], obj[1]))
        win = row["win"]
        total = row["total"]
        return EconomyPlayer(amt, time, bank, interest, pet, win, total)


# asyncpg class for database operations
class db:
    def __init__(self):
        self.count = -1
        self._connection = []

    
    async def connect(self):
        for i in range(5):
            try:
                connection = await asyncpg.connect(DATABASE_URL)
            except:
                pass
            else:
                self._connection.append(connection)
        print(f"HARUKA | Established {len(self._connection)} database connection(s)!")
        await self.initialization()
    

    async def initialization(self):
        await self.conn.execute("""
        CREATE TABLE IF NOT EXISTS economy (id text, amt int, time timestamp, bank int, interest float, pet int[], win int, total int);
        CREATE TABLE IF NOT EXISTS prefix (id text, pref text);
        CREATE TABLE IF NOT EXISTS music (id text, queue text[]);
        """)
        print("HARUKA | Successfully initialized database!")


    async def close(self):
        error = 0
        print("HARUKA | Closing database connections...")
        await asyncio.sleep(3.0)
        for connection in self._connection:
            try:
                await connection.close()
            except Exception as ex:
                print(ex)
                error += 1
        print(f"HARUKA | Attempted to close all database connections, {error} error(s) occured.")
    

    @property
    def conn(self):
        if self.count == 4:
            self.count = 0
        else:
            self.count += 1
        return self._connection[self.count]


# Represents a snippet from a YouTube API search result
class YouTubeSearchResult:
    def __init__(self, json):
        self._json = json
    

    @property
    def id(self):
        return self._json["id"]["videoId"]
    

    @property
    def title(self):
        return self._json["snippet"]["title"]
    

    @property
    def description(self):
        return self._json["snippet"]["description"]
    

    @property
    def channel(self):
        return self._json["snippet"]["channelTitle"]
    

    @property
    def thumbnail(self):
        return self._json["snippet"]["thumbnails"]["high"]["url"]
    

    def embed(self, *args, **kwargs) -> discord.Embed:
        em = discord.Embed(
            title = self.title,
            description = f"{self.channel}\n{self.description}",
            url = f"https://www.youtube.com/watch?v={self.id}",
            color = 0x2ECC71,
        )
        em.set_thumbnail(url=self.thumbnail)
        if kwargs.get("footer"):
            em.set_footer(
                text = kwargs["footer"].get("text") or discord.Embed.Empty,
                icon_url = kwargs["footer"].get("icon_url") or discord.Embed.Empty,
            )
        if kwargs.get("author"):
            em.set_author(
                name = kwargs["author"].get("name") or discord.Embed.Empty,
                icon_url = kwargs["author"].get("icon_url") or discord.Embed.Empty,
            )
        return em


async def prefix(bot, message):
    if str(message.channel.type) == "private":
        return "$"
    elif str(message.channel.type) == "text":
        id = str(message.guild.id)
        row = await bot.db.conn.fetchrow(f"SELECT * FROM prefix WHERE id = '{id}';")
        if not row:
            return "$"
        else:
            return row["pref"]
    else:
        return "$" # No command invoke from on_message


class Haruka(commands.Bot):
    async def start(self, *args, **kwargs):
        await bot.db.connect()
        await super().start(*args)
    

    @staticmethod
    async def giphy(query: str):
        url = f"https://giphy.com/search/{query}"
        lst = []
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
                soup = bs(html, "html.parser")
                obj = str(soup.find(name="body"))
                matches = re.finditer(giphy_pattern_regex, obj)
                for match in matches:
                    if match.group() not in lst:
                        lst.append(match.group())
                    if len(lst) == 15:
                        break
                return lst
            else:
                return ["https://media3.giphy.com/media/hv5AEBpH3ZyNoRnABG/giphy.gif"]
    

    @staticmethod
    async def search(query: str) -> List[YouTubeSearchResult]:
        params = {
            "q": query,
            "type": "video",
            "part": "snippet",
            "key": API_KEY,
            "maxResults": 6,
        }
        async with session.get(f"{youtube_api_url}/search", params=params) as response:
            if response.status == 200:
                json = await response.json()
                items = [YouTubeSearchResult(data) for data in json["items"]]
            else:
                items = []
            return items
    

    @staticmethod
    async def buffer(video_id: str) -> str:
        for url in invidious_urls:
            async with session.get(f"{url}/api/v1/videos/{video_id}") as response:
                if response.status == 200:
                    json = await response.json()
                    sources = [adaptiveFormats["url"] for adaptiveFormats in json["adaptiveFormats"] if adaptiveFormats.get("encoding") == "opus"]
                    return sources[0]
                else:
                    continue


# Initialize bot
intents = discord.Intents.default()
intents.members = True
activity = discord.Activity(type=discord.ActivityType.watching, name="5-year-old animated girls")
bot = Haruka(activity=activity, command_prefix=prefix, intents=intents, case_insensitive=True)
bot.remove_command("help")
bot.db = db()


# Music functions within a voice channel
class Music:
    def __init__(self, channel: discord.VoiceChannel):
        self._channel = channel
    

    @property
    async def queue(self) -> List[str]:
        row = await bot.db.conn.fetchrow(f"SELECT * FROM music WHERE id = '{self._channel.id}';")
        if not row:
            await bot.db.conn.execute(f"INSERT INTO music VALUES ('{self._channel.id}', $1);", [])
            track_ids = []
        else:
            track_ids = row["queue"]
        return track_ids
    

    async def add(self, video_id: str) -> None:
        await bot.db.conn.execute(f"UPDATE music SET queue = array_append(queue, '{video_id}') WHERE id = '{self._channel.id}';")
    

    async def remove(self, pos) -> Optional[str]:
        queue = await self.queue
        try:
            video_id = queue[pos - 1]
        except KeyError:
            pass
        else:
            await bot.db.conn.execute(f"UPDATE music SET queue = array_cat(queue[:{pos - 1}], queue[{pos + 1}:]) WHERE id = '{self._channel.id}';")
            return video_id
    

    async def connect(self) -> discord.VoiceClient:
        vc = self._channel.guild.voice_client
        if vc:
            await vc.disconnect()
            await asyncio.sleep(0.6)
        return await self._channel.connect()
    

    def is_connected(self) -> bool:
        return self._channel.guild.voice_client is not None and self._channel.guild.voice_client.channel.id == self._channel.id


    async def disconnect(self) -> None:
        if self.is_connected():
            await self._channel.guild.voice_client.disconnect()


    async def play(self, url: str) -> None:
        for url in invidious_urls:
            async with session.get(url) as response:
                if response.status == 200:
                    vc = self._channel.guild.voice_client
                    buffer = await response.read()
                    audio = discord.FFmpegOpusAudio(buffer)
                    vc.play(audio)
                    break
                else:
                    continue