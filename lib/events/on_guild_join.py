from lib.settings import *


@bot.event
async def on_guild_join(guild):
    cur.execute("SELECT id FROM prefix;")
    lst = cur.fetchall()
    id = str(guild.id)
    existed = False
    for data in lst:
        if data[0] == id:
            existed = True
            break
    if not existed:
        cur.execute(f"""
        INSERT INTO prefix
        VALUES ('{id}', '$');
        """)
        conn.commit()