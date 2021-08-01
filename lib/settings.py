import aiohttp
import discord
import logging
import os
import psycopg2
from discord.ext import commands
from load import *


# Set up logging
logging.basicConfig(level=logging.INFO)


# Initialize database connection, cursor, root path, side session and max number of processes
TOKEN = os.environ["TOKEN"]
DATABASE_URL = os.environ["DATABASE_URL"]
session = aiohttp.ClientSession()
root = os.getcwd()
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
max_processes = 100


# Initialize database
eco_sql = "CREATE TABLE IF NOT EXISTS economy (id text, amt int, time timestamp, bank int, interest float,"
eco_sql += ",".join(f" pet_{i} int" for i in range(52)) + ", win int, total int);"
pref_sql = "CREATE TABLE IF NOT EXISTS prefix (id text, pref text);"
music_sql = "CREATE TABLE IF NOT EXISTS queue (id text, url text[]);"
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


# Load all existing economy data
cur.execute("SELECT * FROM economy;")
lst = cur.fetchall()
data = {}
for player in lst:
    id = player[0]
    amt = player[1]
    bank_date = player[2]
    bank = player[3]
    interest = player[4]
    pet = [add_pet_data(i - 5, player[i]) for i in range(5, 57)]
    win = player[57]
    total = player[58]
    data[id] = Player(amt, bank_date, bank, interest, pet, win, total)


# Define frequently used emoji lists
checker = ["❌", "✔️"]
choices = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
navigate = ["⬅️", "➡️"]


def prefix(bot, message):
    if str(message.channel.type) == "private":
        id = str(message.channel.id)
    if str(message.channel.type) == "text":
        id = str(message.guild.id)
    cur.execute("SELECT * FROM prefix;")
    lst = cur.fetchall()
    for obj in lst:
        if obj[0] == id:
            return obj[1]


# Initialize bot
intents = discord.Intents.default()
intents.members = True
activity = discord.Game(name="on Heroku")
bot = commands.Bot(activity=activity, command_prefix=prefix, intents=intents, case_insensitive=True)
bot.remove_command("help")
