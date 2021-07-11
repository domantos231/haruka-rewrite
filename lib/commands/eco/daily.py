from discord.ext import commands
from lib.settings import *


@bot.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(cmd):
    id = str(cmd.author.id)
    data[id][0] += 500
    cur.execute(f"""
    UPDATE economy
    SET amt = amt + 500
    WHERE id = '{id}';
    """)
    conn.commit()
    await cmd.send(f"Claimed `💲500` as daily reward!")