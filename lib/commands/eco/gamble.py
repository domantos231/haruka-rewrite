import discord
from discord.ext import commands
from random import randint
from lib.settings import *


@bot.command(name="gamble")
@commands.cooldown(1, 6, commands.BucketType.user)
async def _gamble(cmd, arg: int):
    if arg < 0:
        raise commands.UserInputError
    else:
        id = str(cmd.author.id)
        if arg > data[id][0]:
            await cmd.send("The specified amount of money was greater than your total credits.")
        else:
            i = randint(1, 6)
            j = randint(1, 6)
            if i > j:
                await cmd.send(embed=discord.Embed(title="You lost!", description=f"Bot rolled a **{i}**\n{cmd.author} rolled a **{j}**\nResult: `-💲{arg}`", color=0xF20707))
                data[id][0] -= arg
            elif i == j:
                arg = int(arg/5)
                await cmd.send(embed=discord.Embed(title="Draw!", description=f"Bot rolled a **{i}**\n{cmd.author} rolled a **{j}**\nResult: `+💲{arg}`", color=0xFFFF00))
                data[id][0] += arg
            else:
                await cmd.send(embed=discord.Embed(title="You won!", description=f"Bot rolled a **{i}**\n{cmd.author} rolled a **{j}**\nResult: `+💲{arg}`", color=0x2ECC71))
                data[id][0] += arg
            cur.execute(f"""
            UPDATE economy
            SET amt = {amt}
            WHERE id = '{id}';
            """)
            conn.commit()


@_gamble.error
async def gamble_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")