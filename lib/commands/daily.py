from datetime import datetime
from lib.settings import *


@bot.command()
async def daily(cmd):
    id = cmd.author.id
    ecodb = bot.get_channel(int(ECONOMY_ID))
    async for message in ecodb.history(limit=200):
        data = message.content.split("/")
        if data[0] == str(id):
            date = datetime(int(data[3]), int(data[4]), int(data[5]), 23, 59, 59)
            if datetime.now() > date:
                data[1] = float(data[1]) + 500.0
                data[1] = str(data[1])
                data[3] = str(datetime.now().year)
                data[4] = str(datetime.now().month)
                data[5] = str(datetime.now().day)
                await message.edit(content="/".join(data))
                await cmd.send("Claimed `💲500` as daily reward")
            else:
                await cmd.send("You have claimed today's daily reward.")
            break
