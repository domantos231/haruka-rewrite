import discord
from discord.ext import commands
import os


TOKEN = os.environ["TOKEN"]
ADMIN = os.environ["ADMIN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
ECONOMY_ID = os.environ["ECONOMY_ID"]
choices = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]


async def prefix(bot, message):
    if str(message.channel.type) == "private":
        id = str(message.channel.id)
    if str(message.channel.type) == "text":
        id = str(message.guild.id)
    async for message in db.history(limit=200):
        if message.author == bot.user and message.content.split("=")[0] == id:
            pref = [message.content.split("=")[1]]
            return pref



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
    global db
    db = bot.get_channel(int(CHANNEL_ID))


class stats:
    def __init__(self, i, lv):
        if i * (i - 15) <= 0:  # COMMON
            type = "COMMON"
            a = 1860
            b = 20
            c = 5
            d = 214
            e = 2
        elif (i - 16) * (i - 33) <= 0:  # RARE
            type = "RARE"
            a = 3100
            b = 33
            c = 8
            d = 360
            e = 4
        elif (i - 34) * (i - 47) <= 0:  # EPIC
            type = "EPIC"
            a = 6510
            b = 70
            c = 18
            d = 749
            e = 7
        elif i == 51:  # ????
            type = "????"
            a = 1674000000
            b = 18000000
            c = 4500000
            d = 192600000
            e = 0
        else:  # LEGENDARY
            type = "LEGENDARY"
            a = 120900
            b = 1300
            c = 325
            d = 13910
            e = 50
        self.hp = int(a + b * i + c * lv)
        self.atk = int(d - e * i + c * lv)
        self.type = type


petimg = [
    "🐕",
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
    "🛸",
]
