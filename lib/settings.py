import asyncio
import asyncpg
import aiohttp
import discord
import gc
import logging
import os
import psycopg2
import re
import wavelink
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
from discord.ext import tasks, commands
from load import *


# Set up logging and garbage collector
logging.basicConfig(level=logging.INFO)
gc.enable()


# Initialize database connection, cursor, root path and side session
TOKEN = os.environ["TOKEN"]
DATABASE_URL = os.environ["DATABASE_URL"]
session = aiohttp.ClientSession()
root = os.getcwd()
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()


# Initialize database
eco_sql = "CREATE TABLE IF NOT EXISTS economy (id text, amt int, time timestamp, bank int, interest float, pet int[], win int, total int);"
pref_sql = "CREATE TABLE IF NOT EXISTS prefix (id text, pref text);"
music_sql = "CREATE TABLE IF NOT EXISTS music (id text, queue text[]);"
try:
    cur.execute(eco_sql)
    cur.execute(pref_sql)
    cur.execute(music_sql)
    conn.commit()
except Exception as ex:
    print(f"An exception occured: {ex}")
    print("Exiting program...")
    cur.close()
    conn.close()
    exit()
else:
    print("Successfully initialized database!")


# Define frequently used emoji lists
checker = ["❌", "✔️"]
choices = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
navigate = ["⬅️", "➡️"]


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
        return Player(amt, time, bank, interest, pet, win, total)


# Load all action commands' GIFs from giphy
giphy_pattern_regex = r'(?=(http://|https://))[^"|?]+giphy[.]gif'
class GIF:
    def __init__(self, query):
        self.query = query


    async def giphy_leech(self):
        url = f"https://giphy.com/search/{self.query}"
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


# asyncpg class for database connection
class db:
    def __init__(self):
        pass

    
    async def connect(self):
        self._connection = await asyncpg.connect(DATABASE_URL)
        print(f"asyncpg connected to database!\: {self._connection}")
    

    async def close(self):
        await self._connection.close()
    

    @property
    def conn(self):
        return self._connection


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


# Initialize bot
intents = discord.Intents.default()
intents.members = True
activity = discord.Game(name="nothing")
bot = commands.Bot(activity=activity, command_prefix=prefix, intents=intents, case_insensitive=True)
bot.remove_command("help")
if not hasattr(bot, "wavelink"):
    bot.wavelink = wavelink.Client(bot=bot)
if not hasattr(bot, "db"):
    bot.db = db()


# Keep lavalink server running (maybe?)
@tasks.loop(seconds=1800.0)
async def keep_alive():
    tracks = await bot.wavelink.get_tracks(f"ytsearch:just some random stuff here")
    del tracks
    gc.collect()
    print(f"Finished keep_alive task at {dt.now()}")


# Initialize wavelink nodes
async def start_nodes():
    await bot.wait_until_ready()
    await bot.wavelink.initiate_node(
        host = "127.0.0.1",
        port = 2333,
        rest_uri = "http://127.0.0.1:2333",
        password = os.environ["PASSWORD"],
        identifier = "Haruka Wavelink Client",
        region = "hongkong",
    )
    try:
        keep_alive.start()
    except:
        pass
bot.loop.create_task(start_nodes())
