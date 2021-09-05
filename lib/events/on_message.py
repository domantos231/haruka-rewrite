from settings import *
from objects import *


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if isinstance(message.channel, discord.TextChannel):
        id = message.guild.id
        row = await bot.db.conn.fetchrow(f"SELECT * FROM prefix WHERE id = '{id}';")
        if not row:
            await bot.db.conn.execute(f"""
            INSERT INTO prefix (id, pref)
            VALUES ('{id}', '$');
            """)
    if isinstance(message.channel, discord.TextChannel) or isinstance(message.channel, discord.DMChannel):
        await bot.process_commands(message)
