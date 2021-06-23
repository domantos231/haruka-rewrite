import discord
from discord.ext import commands
from random import randint
from lib.settings import *


@bot.command()
async def gamble(cmd, arg: int):
    if arg < 0:
        raise commands.UserInputError
    else:
        arg = float(arg)
        ecodb = bot.get_channel(int(ECONOMY_ID))
        async for message in ecodb.history(limit=200):
            data = message.content.split("/")
            if data[0] == str(cmd.author.id):
                amt = float(data[1])
                if arg > amt:
                    await cmd.send("The specified amount of money was greater than your total credits.")
                else:
                    i = randint(1, 6)
                    j = randint(1, 6)
                    if i > j:
                        await cmd.send(embed=discord.Embed(title="You lost!", description=f"Bot rolled a **{i}**\n{cmd.author} rolled a **{j}**\nResult: `-💲{int(arg)}`", color=0xF20707))
                        amt -= arg
                    elif i == j:
                        arg = int(arg/2)
                        await cmd.send(embed=discord.Embed(title="Draw!", description=f"Bot rolled a **{i}**\n{cmd.author} rolled a **{j}**\nResult: `-💲{int(arg)}`", color=0xFFFF00))
                        amt -= arg
                    else:
                        await cmd.send(embed=discord.Embed(title="You won!", description=f"Bot rolled a **{i}**\n{cmd.author} rolled a **{j}**\nResult: `+💲{int(arg)}`", color=0x2ECC71))
                        amt += arg
                    data[1] = str(amt)
                    await message.edit(content="/".join(data))
                break


@gamble.error
async def gamble_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")