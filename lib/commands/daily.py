from discord.ext import commands
from datetime import datetime as dt
from lib.settings import *


@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def daily(cmd):
    id = str(cmd.author.id)
    now = dt.now()
    date = dt(data[id][1], data[id][2], data[id][3], 23, 59, 59)
    if now > date:
        data[id][0] += 500
        data[id][1] = now.year
        data[id][2] = now.month
        data[id][3] = now.day
        cur.execute(f"""
        UPDATE economy
        SET amt = amt + 500, year = {now.year}, month = {now.month}, day = {now.day}
        WHERE id = '{id}';
        """)
        conn.commit()
        await cmd.send(f"Claimed `💲500` as daily reward!\nCurrent server time is **{now}**")
    else:
        await cmd.send(f"You have claimed today's login reward!\nCurrent server time is **{now}**")