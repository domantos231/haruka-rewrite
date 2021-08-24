from discord.ext import commands
from settings import *


@bot.command(
    name = "daily",
    description = "Claim your daily reward",
)
@commands.cooldown(1, 86400, commands.BucketType.user)
async def _daily(cmd):
    id = cmd.author.id
    await bot.db.conn.execute(f"""
    UPDATE economy
    SET amt = amt + 500
    WHERE id = '{id}';
    """)
    await cmd.send(f"Claimed `💲500` as daily reward!")