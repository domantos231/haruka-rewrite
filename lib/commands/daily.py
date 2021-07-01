from datetime import datetime as dt
from lib.settings import *


@bot.command()
async def daily(cmd):
    id = str(cmd.author.id)
    cur.execute("SELECT * FROM economy;")
    lst = cur.fetchall()
    for data in lst:
        if data[0] == id:
            date = dt(data[2], data[3], data[4], 23, 59, 59)
            if dt.now() > date:
                now = dt.now()
                cur.execute(f"""
                UPDATE economy
                SET amt = {500 + data[1]}, year = {now.year}, month = {now.month}, day = {now.day}
                WHERE id = '{id}';
                """)
                conn.commit()
                await cmd.send("Claimed `💲500` as daily reward")
            else:
                await cmd.send("You have claimed today's daily reward.")
            break
