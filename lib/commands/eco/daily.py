from discord.ext import commands
from settings import *


@bot.command(name="daily")
@commands.cooldown(1, 86400, commands.BucketType.user)
async def _daily(cmd):
    id = str(cmd.author.id)
    player = data[id]
    player.amt += 500
    cur.execute(f"""
    UPDATE economy
    SET amt = amt + 500
    WHERE id = '{id}';
    """)
    conn.commit()
    await cmd.send(f"Claimed `💲500` as daily reward!")