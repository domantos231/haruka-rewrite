import datetime
import discord
from datetime import datetime as dt
from settings import *


@bot.group(name="bank", case_insensitive=True)
@commands.cooldown(1, 3, commands.BucketType.user)
async def _bank(cmd):
    id = cmd.author.id
    player = await data(id).player
    if not player.time:
        player.time = dt.now()
        await bot.db.conn.execute(
            f"UPDATE economy SET time = $1 WHERE id = '{id}';",
            dt.now()
        )
    if cmd.invoked_subcommand is None:
        delta = dt.now() - player.time
        hours = 24 * delta.days + int(delta.seconds / 3600)
        money = int(player.bank * pow(1 + player.interest/100, hours))
        em = discord.Embed(title="🏦 WELCOME TO THE BANK", description=f"Your bank account `💲{money}`\nInterest `{player.interest}%/h`", color=0x2ECC71)
        em.set_author(name=cmd.author.name, icon_url=cmd.author.avatar_url)
        em.set_footer(text=f"{hours} hours since last transaction.")
        await cmd.send(embed=em)


@_bank.command(name="deposit")
async def _deposit(cmd, arg):
    id = cmd.author.id
    player = await data(id).player
    if not player.time:
        player.time = dt.now()
        await bot.db.conn.execute(
            f"UPDATE economy SET time = $1 WHERE id = '{id}';",
            dt.now()
        )
    try:
        arg = int(arg)
    except ValueError:
        if arg.lower() == "all":
            arg = player.amt
        else:
            return await cmd.send("Please specify a valid amount of money to deposit")
    delta = dt.now() - player.time
    hours = 24 * delta.days + int(delta.seconds / 3600)
    money = int(player.bank * pow(1 + player.interest/100, hours))
    if arg > player.amt:
        await cmd.send(f"<@!{id}> You don't have enough money!")
    else:
        await bot.db.conn.execute(f"""
        UPDATE economy
        SET amt = amt - {arg}, bank = {money} + {arg}, time = $1
        WHERE id = '{id}';
        """, dt.now())
        await cmd.send(f"<@!{id}> sent `💲{arg}` to the bank.")


@_bank.command(name="withdraw")
async def _withdraw(cmd, arg):
    id = cmd.author.id
    player = await data(id).player
    if not player.time:
        player.time = dt.now()
        await bot.db.conn.execute(
            f"UPDATE economy SET time = $1 WHERE id = '{id}';",
            dt.now()
        )
    delta = dt.now() - player.time
    hours = 24 * delta.days + int(delta.seconds / 3600)
    money = int(player.bank * pow(1 + player.interest/100, hours))
    try:
        arg = int(arg)
    except ValueError:
        if arg.lower() == "all":
            arg = money
        else:
            return await cmd.send("Please specify a valid amount of money to withdraw")
    if arg > money:
        await cmd.send(f"<@!{id}> You don't have enough money in your bank account!")
    else:
        await bot.db.conn.execute(f"""
        UPDATE economy
        SET amt = amt + {arg}, bank = {money} - {arg}, time = $1
        WHERE id = '{id}';
        """, dt.now())
        await cmd.send(f"<@!{id}> withdrew `💲{arg}` from the bank.")
