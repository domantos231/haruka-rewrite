import asyncio
import asyncpg
import aiohttp
import discord
import gc
import logging
import os
import re
import wavelink
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
from discord.ext import tasks, commands
from typing import *
from load import *


# Set up logging and garbage collector
logging.basicConfig(level=logging.INFO)
gc.enable()


# Initialize environment variables
TOKEN = os.environ["TOKEN"]
DATABASE_URL = os.environ["DATABASE_URL"]


# Define frequently used emoji lists
checker = ["❌", "✔️"]
choices = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
navigate = ["⬅️", "➡️"]


# Define giphy RegEx pattern
giphy_pattern_regex = r'(?=(http://|https://))[^"|?]+giphy[.]gif'


# asyncpg class for database connection
class db:
    _maximum_connections = 10
    def __init__(self):
        self.count = -1
        self._connection = []

    
    async def connect(self):
        for i in range(self._maximum_connections):
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
        for connection in self._connection:
            try:
                await connection.close()
            except Exception as ex:
                print(ex)
                error += 1
        print(f"HARUKA | Attempted to close all database connections, {error} error(s) occured.")
    

    @property
    def conn(self):
        if self.count == self._maximum_connections - 1:
            self.count = 0
        else:
            self.count += 1
        return self._connection[self.count]


async def prefix(bot, message):
    if isinstance(message.channel, discord.DMChannel):
        return "$"
    elif isinstance(message.channel, discord.TextChannel):
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
        await self.db.connect()
        self.wordlist = ["pneumonoultramicroscopicsilicovolcanoconiosis", "antidisestablishmentarianism"]
        async with aiohttp.ClientSession() as session:
            self.session = session
            prelist = await self.get_wordlist()
            for word in prelist:
                self.wordlist.append(word.lower())
            del prelist
            print(f"HARUKA | Fetched wordlist with {len(self.wordlist)} words.")
            await super().start(*args, **kwargs)
    

    async def get_wordlist(self):
        async with self.session.get("https://www.ef.com/wwen/english-resources/english-vocabulary/top-3000-words/") as response:
            if response.status == 200:
                html = await response.text()
                soup = bs(html, "html.parser")
                obj = soup.find(name="section", attrs={"class": "col-md-12"}).find_all("p")[1]
                return obj.get_text(separator=r"%").split(r"%")
            else:
                print(f"HARUKA | Wordlist site retured status code {response.status}. Using default words.")
                return ["pneumonoultramicroscopicsilicovolcanoconiosis", "antidisestablishmentarianism"]
    

    async def giphy(self, query: str):
        url = f"https://giphy.com/search/{query}"
        lst = []
        async with self.session.get(url) as response:
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
    async def get_player(id):
        row = await bot.db.conn.fetchrow(f"SELECT * FROM economy WHERE id = '{id}';")
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
    

# Initialize bot
intents = discord.Intents.default()
intents.members = True
activity = discord.Activity(type=discord.ActivityType.watching, name="5-year-old animated girls")
bot = Haruka(activity=activity, command_prefix=prefix, intents=intents, case_insensitive=True)
bot.remove_command("help")
bot.db = db()


# Initialize wavelink nodes
async def start_nodes():
    await bot.wait_until_ready()
    bot.node = await wavelink.NodePool.create_node(
        bot = bot,
        host = "lava.link",
        port = 80,
        password = "anything as a password",
        region = "hongkong",
    )
bot.loop.create_task(start_nodes())


# Music function within a channel
class Music:
    def __init__(self, channel: discord.VoiceChannel):
        self.channel = channel
    

    @property
    async def queue(self) -> List[str]:
        row = await bot.db.conn.fetchrow(f"SELECT * FROM music WHERE id = '{self.channel.id}';")
        if not row:
            await bot.db.conn.execute(f"INSERT INTO music VALUES ('{self.channel.id}', $1);", [])
            track_ids = []
        else:
            track_ids = row["queue"]
        return track_ids
    

    @property
    def player(self) -> Optional[wavelink.Player]:
        return bot.node.get_player(self.channel.guild)
    

    async def connect(self) -> None:
        if self.player and self.player.is_connected():
            await self.player.disconnect(force=True)
            await asyncio.sleep(0.6)
        await self.channel.connect(cls=wavelink.Player)
    

    async def add(self, track: wavelink.YouTubeTrack) -> None:
        await bot.db.conn.execute(f"UPDATE music SET queue = array_append(queue, '{track.id}') WHERE id = '{self.channel.id}';")
            

    async def remove(self, pos) -> Optional[wavelink.YouTubeTrack]:
        queue = await self.queue
        try:
            track_id = queue[pos - 1]
            if pos < 1:
                raise IndexError
        except IndexError:
            pass
        else:
            await bot.db.conn.execute(f"UPDATE music SET queue = array_cat(queue[:{pos - 1}], queue[{pos + 1}:]) WHERE id = '{self.channel.id}';")
            track = await bot.node.build_track(cls=wavelink.YouTubeTrack, identifier=track_id)
            return track
    

    async def play(self, track: wavelink.YouTubeTrack) -> None:
        if self.player is not None:
            await self.player.play(track)
            await asyncio.sleep(0.4)
            while self.player.is_connected() and self.player.position < track.length:
                await asyncio.sleep(0.4)
