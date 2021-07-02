import discord
from psycopg2 import *
from discord.ext import commands
import os


TOKEN = os.environ["TOKEN"]
DATABASE_URL = os.environ["DATABASE_URL"]


conn = connect(DATABASE_URL)
cur = conn.cursor()
eco_sql = "CREATE TABLE IF NOT EXISTS economy (id text, amt int, year int, month int, day int,"
add = []
for i in range(52):
    add.append(f" pet_{i} int")
eco_sql += ",".join(add) + ", win int, total int);"
pref_sql = "CREATE TABLE IF NOT EXISTS prefix (id text, pref text);"
try:
    cur.execute(eco_sql)
    cur.execute(pref_sql)
    conn.commit()
except Exception as ex:
    print(f"An exception occured: {ex}")
    print("Exiting program...")
    cur.close()
    conn.close()
    exit()
else:
    print("Successfully connected to database!")
    del eco_sql
    del pref_sql
    del add
    cur.execute("SELECT * FROM economy;")
    lst = cur.fetchall()
    data = {}
    for i in lst:
        data[i[0]] = list(i[1:])
    del lst
    print("Initialization completed.")


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


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=prefix, intents=intents, case_insensitive=True)
bot.remove_command("help")


@bot.event
async def on_connect():
    print("Connected to Discord!")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="on heroku"))


choices = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]


class stats:
    def __init__(self, i, lv):
        if i * (i - 15) <= 0:  # COMMON
            type = "COMMON"
            hp = 3000 + 50 * (i - 7) + 5 * (i + 1) * lv
            atk = 1000 + 20 * (7 - i) + 5 * (16 - i) * lv
        elif (i - 16) * (i - 33) <= 0:  # RARE
            type = "RARE"
            hp = 3200 + 50 * (i - 24) + 6 * (i - 14) * lv
            atk = 1200 + 20 * (24 - i) + 6 * (35 - i) * lv
        elif (i - 34) * (i - 47) <= 0:  # EPIC
            type = "EPIC"
            hp = 4000 + 60 * (i - 40) + 9 * (i - 40) * lv
            atk = 1800 + 30 * (40 - i) + 8 * (50 - i) * lv
        elif i == 51:  # ????
            type = "????"
            hp = 70000 + 2000 * lv
            atk = 40000 + 1200 * lv
        else:  # LEGENDARY
            type = "LEGENDARY"
            hp = 7000 + 180 * (i - 49) + 12 * (i - 49) * lv
            atk = 3000 + 90 * (49 - i) + 12 * (52 - i) * lv
        self.hp = hp
        self.atk = atk
        self.type = type


petimg = ["🐕",
    "🐈",
    "🐂",
    "🐃",
    "🐄",
    "🐖",
    "🐪",
    "🐁",
    "🐇",
    "🐓",
    "🐦",
    "🦆",
    "🦎",
    "🐟",
    "🐌",
    "🦀",
    "🦮",
    "🐕‍🦺",
    "🐎",
    "🐏",
    "🐑",
    "🐐",
    "🐫",
    "🦙",
    "🦇",
    "🦨",
    "🐧",
    "🕊️",
    "🦢",
    "🦜",
    "🐢",
    "🐍",
    "🐡",
    "🐝",
    "🐩",
    "🐈‍⬛",
    "🐅",
    "🐆",
    "🐘",
    "🦛",
    "🦉",
    "🦚",
    "🐊",
    "🐋",
    "🐬",
    "🦈",
    "🐙",
    "🦑",
    "🐉",
    "🦕",
    "🦖",
    "🛸",]
