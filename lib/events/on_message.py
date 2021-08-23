from settings import *
from load import *


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if bot.user.mentioned_in(message):
        if isinstance(message.channel, discord.TextChannel):
            id = message.guild.id
            row = await bot.db.conn.fetchrow(f"SELECT * FROM prefix WHERE id = '{id}';")
            pref = row["pref"]
            await message.channel.send(f"My current prefix is: {pref}")
        elif isinstance(message.channel, discord.DMChannel):
            await message.channel.send("My current prefix is: $")
        else:
            await cmd.send("This channel type is not supported.")
    if isinstance(message.channel, discord.TextChannel):
        try:
            id = message.guild.id
        except:
            pass
        else:
            row = await bot.db.conn.fetchrow(f"SELECT * FROM prefix WHERE id = '{id}';")
            if not row:
                await bot.db.conn.execute(f"""
                INSERT INTO prefix (id, pref)
                VALUES ('{id}', '$');
                """)
    id = message.author.id
    if not await bot.get_player(id):
        await bot.db.conn.execute(
            f"INSERT INTO economy VALUES ('{id}', 300, NULL, 0, 1.01, $1, 0, 0)",
            [0] * 52
        )
    if isinstance(message.channel, discord.TextChannel) or isinstance(message.channel, discord.DMChannel):
        await bot.process_commands(message)
