from lib.settings import *


@bot.event
async def on_disconnect():
    cur.close()
    conn.close()
    print("Disconnected")