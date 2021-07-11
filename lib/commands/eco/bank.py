import datetime
import discord
from datetime import datetime as dt
from lib.settings import *


@bot.command()
async def bank(cmd, *args):
    id = str(cmd.author.id)
    if data[id][1] is None:
        data[id][1] = dt.now()
        cur.execute(f"""
        UPDATE economy
        SET time = '{dt.now()}'
        WHERE id = '{id}';
        """)
        conn.commit()
        money = 0
    else:
        i = data[id][3]
        delta = dt.now() - data[id][1]
        n = 24 * delta.days + int(delta.seconds / 3600)
        money = int(data[id][2] * pow(1 + i/100, n))
    if len(args) == 0:
        em = discord.Embed(title="🏦 WELCOME TO THE BANK", description=f"Your bank account `💲{money}`\nInterest `{data[id][3]}%/h`", color=0x2ECC71)
        em.set_author(name=cmd.author.name, icon_url=cmd.author.avatar_url)
        await cmd.send(embed=em)
    elif args[0].lower() == "deposit":
        try:
            deposit = int(args[1])
            if deposit < 0:
                raise ValueError
        except:
            if args[1].lower() == "all":
                deposit = data[id][0]
            else:
                await cmd.send("Please check your input again.")
                return
        if deposit > data[id][0]:
            await cmd.send(f"<@!{id}> You don't have enough money!")
        else:
            data[id][1] = dt.now()
            data[id][2] = money
            data[id][0] -= deposit
            data[id][2] += deposit
            cur.execute(f"""
            UPDATE economy
            SET amt = amt - {deposit}, time = '{dt.now()}', bank = {data[id][2]}
            WHERE id = '{id}';
            """)
            conn.commit()
            await cmd.send(f"<@!{id}> sent `💲{deposit}` to the bank.")
    elif args[0].lower() == "withdraw":
        try:
            withdraw = int(args[1])
            if withdraw < 0:
                raise ValueError
        except:
            if args[1].lower() == "all":
                withdraw = data[id][2]
            else:
                await cmd.send("Please check your input again.")
                return
        if withdraw > money:
            await cmd.send(f"<@!{id}> Your bank account doesn't have enough money!")
        else:
            data[id][1] = dt.now()
            data[id][2] = money
            data[id][0] += withdraw
            data[id][2] -= withdraw
            cur.execute(f"""
            UPDATE economy
            SET amt = amt - {withdraw}, time = '{dt.now()}', bank = {data[id][2]}
            WHERE id = '{id}';
            """)
            conn.commit()
            await cmd.send(f"<@!{id}> withdrew `💲{withdraw}` from the bank.")
