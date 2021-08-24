import discord
from discord.ext import commands
from random import randint
from settings import *


@bot.command(
    name = "dice",
    description = "Dice gambling",
    usage = "dice <amount>",
)
@commands.cooldown(1, 10, commands.BucketType.user)
async def _dice(cmd, arg):
    id = cmd.author.id
    player = await bot.get_player(id)
    try:
        arg = int(arg)
    except ValueError:
        if arg.lower() == "all":
            arg = player.amt
        else:
            raise commands.UserInputError
    if arg < 0:
        raise commands.UserInputError
    else:
        if arg > player.amt:
            await cmd.send("The specified amount of money was greater than your total credits.")
        else:
            i = randint(1, 6)
            j = randint(1, 6)
            if i > j:
                await cmd.send(embed=discord.Embed(title="You lost!", description=f"Bot rolled a **{i}**\n{cmd.author} rolled a **{j}**\nResult: `-💲{arg}`", color=0xF20707))
                player.amt -= arg
            elif i == j:
                arg = int(arg/5)
                await cmd.send(embed=discord.Embed(title="Draw!", description=f"Bot rolled a **{i}**\n{cmd.author} rolled a **{j}**\nResult: `+💲{arg}`", color=0xFFFF00))
                player.amt += arg
            else:
                await cmd.send(embed=discord.Embed(title="You won!", description=f"Bot rolled a **{i}**\n{cmd.author} rolled a **{j}**\nResult: `+💲{arg}`", color=0x2ECC71))
                player.amt += arg
            await bot.db.conn.execute(f"""
            UPDATE economy
            SET amt = {player.amt}
            WHERE id = '{id}';
            """)
