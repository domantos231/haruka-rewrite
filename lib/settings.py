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
discord_logger = logging.getLogger("discord")
discord_logger.setLevel(logging.INFO)
discord_logger.addHandler(logging.FileHandler(filename="log.txt", mode="a"))
wavelink_logger = logging.getLogger("wavelink")
wavelink_logger.setLevel(logging.INFO)
wavelink_logger.addHandler(logging.FileHandler(filename="log.txt", mode="a"))
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
    print("Successfully initialized database!")
except Exception as ex:
    print(f"An exception occured: {ex}")
    print("Exiting program...")
    exit()
finally:
    cur.close()
    conn.close()    


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
        print(f"Established {len(self._connection)} database connection(s):\n" + "\n".join(f"{connection}" for connection in self._connection))
    

    async def close(self):
        error = 0
        for connection in self._connection:
            try:
                await connection.close()
            except:
                error += 1
            finally:
                print(f"Closed all database conenctions, {error} error(s) occured.")
    

    @property
    def conn(self):
        if self.count == 4:
            self.count = 0
        else:
            self.count += 1
        return self._connection[self.count]


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
activity = discord.Activity(type=discord.ActivityType.watching, name="5-year-old animated girls")
bot = commands.Bot(activity=activity, command_prefix=prefix, intents=intents, case_insensitive=True)
bot.remove_command("help")
if not hasattr(bot, "wavelink"):
    bot.wavelink = wavelink.Client(bot=bot)
if not hasattr(bot, "db"):
    bot.db = db()


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
bot.loop.create_task(start_nodes())
