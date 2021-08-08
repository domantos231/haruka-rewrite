from settings import *


@bot.event
async def on_guild_join(guild):
    id = guild.id
    row = bot.db.conn.fetchrow(f"SELECT id FROM prefix WHERE id = '{id}';")
    if not row:
        await bot.db.conn.execute(f"""
        INSERT INTO prefix
        VALUES ('{id}', '$');
        """)