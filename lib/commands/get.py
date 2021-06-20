import discord
from discord.ext import commands
from lib.settings import *


@bot.command()
async def get(cmd, arg, user: discord.User = None):
    if not cmd.author.id == int(ADMIN):
        await cmd.send("This command is available for developers only.")
        return
    if user == None:
        user = cmd.author
    try:
        arg = float(arg)
    except:
        await cmd.send("Please specify an amount of money!")
    else:
        id = user.id
        if user.bot:
            await cmd.send(f"<@!{id}> is a bot user!")
        else:
            null = True
            ecodb = bot.get_channel(int(ECONOMY_ID))
            async for message in ecodb.history(limit=200):
                data = message.content.split("/")
                if data[0] == str(id):
                    null = False
                    amt = float(data[1])
                    amt += arg
                    data[1] = str(amt)
                    dat = ""
                    for i in range(59):
                        dat += data[i] + "/"
                    dat += data[59]
                    await message.edit(content=dat)
                    await cmd.send(embed=discord.Embed(title="Request accepted", description="Successfully generated `💲{:.1f}`".format(arg) + f" for <@!{id}>", color=0x2ECC71))
                    break
            if null:
                await cmd.send("This user has no data in my database.")


@get.error
async def get_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check yout input again.")