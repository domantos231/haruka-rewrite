from discord.ext import commands
from settings import *


@bot.command(
    name = "daily",
    description = "Claim your daily reward",
)
@commands.cooldown(1, 86400, commands.BucketType.user)
async def _daily(cmd):
    id = cmd.author.id
    if not await bot.get_player(id):
        await bot.db.conn.execute(
            f"INSERT INTO economy VALUES ('{id}', 300, NULL, 0, 1.01, $1, 0, 0)",
            [0] * 52
        )
    await bot.db.conn.execute(f"""
    UPDATE economy
    SET amt = amt + 500
    WHERE id = '{id}';
    """)
    await cmd.send(f"Claimed `💲500` as daily reward!")