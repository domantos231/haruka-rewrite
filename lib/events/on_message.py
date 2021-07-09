from lib.settings import *


add = ", NULL, 0, 1.01"
for i in range(54):
    add += ", 0"


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if bot.user.mentioned_in(message):
        if str(message.channel.type) == "private":
            id = str(message.channel.id)
        if str(message.channel.type) == "text":
            id = str(message.guild.id)
        cur.execute("SELECT * FROM prefix;")
        lst = cur.fetchall()
        for obj in lst:
            if obj[0] == id:
                await message.channel.send(f"My current prefix is: {obj[1]}")
                break
    if str(message.channel.type) == "private":
        existed = False
        id = str(message.channel.id)
        cur.execute("SELECT id FROM prefix;")
        lst = cur.fetchall()
        for obj in lst:
            if obj[0] == id:
                existed = True
                break
        if not existed:
            cur.execute(f"""
            INSERT INTO prefix (id, pref)
            VALUES ('{id}', '$');
            """)
            conn.commit()
    id = str(message.author.id)
    try:
        data[id]
    except:
        eco_sql = f"""
        INSERT INTO economy
        VALUES ('{id}', 300{add});
        """
        cur.execute(eco_sql)
        conn.commit()
        data[id] = [300, None, 0, 1.01]
        for i in range(54):
            data[id].append(0)
    await bot.process_commands(message)
