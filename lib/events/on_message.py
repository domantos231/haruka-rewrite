from lib.settings import *


@bot.event
async def on_message(message):
    db = bot.get_channel(int(CHANNEL_ID))
    ecodb = bot.get_channel(int(ECONOMY_ID))
    if message.author.bot:
        return
    if bot.user.mentioned_in(message):
        if str(message.channel.type) == "private":
            id = str(message.channel.id)
        if str(message.channel.type) == "text":
            id = str(message.guild.id)
        async for msg in db.history(limit=200):
            if msg.author == bot.user and msg.content.split("=")[0] == id:
                await message.channel.send(
                    "My current prefix is: {0}".format(msg.content.split("=")[1])
                )
    if str(message.channel.type) == "private":
        existed = False
        id = str(message.channel.id)
        async for msg in db.history(limit=200):
            if msg.author == bot.user and msg.content.split("=")[0] == id:
                existed = True
                break
        if not existed:
            await db.send(id + "=$")
    existed = False
    async for msg in ecodb.history(limit=200):
        if msg.content.split("/")[0] == str(message.author.id):
            existed = True
            break
    if not existed:
        eco_str = str(message.author.id) + "/300/0/1/1/1"
        for i in range(52):
            eco_str += "/0"
        eco_str += "/0/0"
        await ecodb.send(eco_str)
    await bot.process_commands(message)
