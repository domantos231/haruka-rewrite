from settings import *
from load import *


pet_add = "array[" + ", ".join("0" for i in range(52)) + "]"
add = f", NULL, 0, 1.01, {pet_add}, 0, 0"


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if bot.user.mentioned_in(message):
        if str(message.channel.type) == "text":
            id = message.guild.id
            cur.execute(f"""
            SELECT *
            FROM prefix
            WHERE id = '{id}';
            """)
            lst = cur.fetchall()
            pref = lst[0][1]
        else:
            pref = "$"
        await message.channel.send(f"My current prefix is: {pref}")
    if str(message.channel.type) == "text":
        try:
            id = str(message.guild.id)
        except:
            id = None
        cur.execute(f"""
        SELECT id
        FROM prefix
        WHERE id = '{id}';
        """)
        lst = cur.fetchall()
        if len(lst) == 0:
            cur.execute(f"""
            INSERT INTO prefix (id, pref)
            VALUES ('{id}', '$');
            """)
            conn.commit()
    id = str(message.author.id)
    if not data(id).player():
        eco_sql = f"""
        INSERT INTO economy
        VALUES ('{id}', 300{add});
        """
        cur.execute(eco_sql)
        conn.commit()
    await bot.process_commands(message)
