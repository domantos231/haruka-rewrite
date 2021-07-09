import discord
from psycopg2 import *
from discord.ext import commands
import os


TOKEN = os.environ["TOKEN"]
DATABASE_URL = os.environ["DATABASE_URL"]


conn = connect(DATABASE_URL)
cur = conn.cursor()
eco_sql = "CREATE TABLE IF NOT EXISTS economy (id text, amt int, time timestamp, bank int, interest float,"
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
activity = discord.Game(name="on Heroku")
bot = commands.Bot(activity=activity, command_prefix=prefix, intents=intents, case_insensitive=True)
bot.remove_command("help")


@bot.event
async def on_connect():
    print("Connected to Discord!")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


choices = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]
effect = []
def calc0(lv):
    if lv == 1:
        return "When receiving damage: 5% chance to ignore 150 damage", 5, 150
    else:
        rate = 4 + 19 * calc0(lv - 1)[1] / 20
        rate_display = "{:.2f}".format(rate)
        reduction = 140 + 10 * lv
        return f"When receiving damage: {rate_display}% chance to ignore {reduction} damage", rate, reduction
effect.append(calc0) # ID 0
def calc1(lv):
    heal = 45 + 5 * lv
    return f"At the end of turn: restore {heal} HP", None, heal
effect.append(calc1) # ID 1
def calc2(lv):
    if lv == 1:
        return "At the end of turn: 10% chance to restore 100 HP", 10, 100
    else:
        rate = 4 + 19 * calc2(lv - 1)[1] / 20
        rate_display = "{:.2f}".format(rate)
        heal = 90 + 10 * lv
        return f"At the end of turn: {rate_display}% chance to restore {heal} HP", rate, heal
effect.append(calc2) # ID 2
def calc3(lv):
    if lv == 1:
        return "At the end of turn: 5% chance to restore 50 HP for all team", 5, 50
    else:
        rate = 4 + 19 * calc3(lv - 1)[1] / 20
        rate_display = "{:.2f}".format(rate)
        heal = 42 + 8 * lv
        return f"At the end of turn: {rate_display}% chance to restore {heal} HP for all team", rate, heal
effect.append(calc3) # ID 3
def calc4(lv):
    heal = 36 + 4 * lv
    return f"At the end of turn: restore {heal} HP to all team members", None, heal
effect.append(calc4) # ID 4
def calc5(lv):
    if lv == 1:
        return "When this pet is defeated: 2% chance to revive with 50 HP", 2, 50
    else:
        rate = 2 + 39 * calc5(lv - 1)[1] / 40
        rate_display = "{:.2f}".format(rate)
        revive = 45 + 5 * lv
        return f"When this pet is defeated: {rate_display}% chance to revive with {revive} HP", rate, revive
effect.append(calc5) # ID 5
def calc6(lv):
    if lv == 1:
        return "When this pet attacks: deal extra damage equal to 2% current HP", 2, None
    else:
        rate = 2 + 39 * calc6(lv - 1)[1] / 40
        rate_display = "{:.2f}".format(rate)
        return f"When this pet attacks: deal extra damage equal to {rate_display}% current HP", rate, None
effect.append(calc6) # ID 6


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
        try:
            eff, eff_rate, eff_value = effect[i](lv)
        except:
            eff, eff_rate, eff_value = (None, None, None)
        self.eff = eff
        self.eff_rate = eff_rate
        self.eff_value = eff_value


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
