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
