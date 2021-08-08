from settings import *
from load import *


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if bot.user.mentioned_in(message):
        if str(message.channel.type) == "text":
            id = message.guild.id
            row = await bot.db.conn.fetchrow(f"SELECT * FROM prefix WHERE id = '{id}';")
            pref = row["pref"]
            await message.channel.send(f"My current prefix is: {pref}")
        elif str(message.channel.type) == "private":
            await message.channel.send("My current prefix is: $")
        else:
            await cmd.send("This channel type is not supported.")
    if str(message.channel.type) == "text":
        try:
            id = str(message.guild.id)
        except:
            pass
        else:
            row = await bot.db.conn.fetchrow(f"SELECT * FROM prefix WHERE id = '{id}';")
            if not row:
                await bot.db.conn.execute(f"""
                INSERT INTO prefix (id, pref)
                VALUES ('{id}', '$');
                """)
    id = str(message.author.id)
    if not await data(id).player:
        await bot.db.conn.execute(
            f"INSERT INTO economy VALUES ('{id}', 300, NULL, 0, 1.01, $1, 0, 0)",
            [0 for i in range(52)]
        )
    if str(message.channel.type) in ["private", "text"]:
        await bot.process_commands(message)
