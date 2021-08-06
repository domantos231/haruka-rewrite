import datetime
import discord
from datetime import datetime as dt
from settings import *


@bot.command(name="bank")
@commands.cooldown(1, 3, commands.BucketType.user)
async def _bank(cmd, *args):
    id = str(cmd.author.id)
    player = data[id]
    if player.bank_date is None:
        player.bank_date = dt.now()
        cur.execute(f"""
        UPDATE economy
        SET time = '{player.bank_date}'
        WHERE id = '{id}';
        """)
        conn.commit()
        money = 0
    else:
        delta = dt.now() - player.bank_date
        hours = 24 * delta.days + int(delta.seconds / 3600)
        money = int(player.bank * pow(1 + player.interest/100, hours))
    if len(args) == 0:
        em = discord.Embed(title="🏦 WELCOME TO THE BANK", description=f"Your bank account `💲{money}`\nInterest `{player.interest}%/h`", color=0x2ECC71)
        em.set_author(name=cmd.author.name, icon_url=cmd.author.avatar_url)
        await cmd.send(embed=em)
    elif args[0].lower() == "deposit":
        try:
            deposit = int(args[1])
            if deposit < 0:
                raise ValueError
        except KeyError:
            await cmd.send("Please specify a deposit amount")
            return
        except ValueError:
            if args[1].lower() == "all":
                deposit = player.amt
            else:
                await cmd.send("Please check your input again.")
                return
        if deposit > player.amt:
            await cmd.send(f"<@!{id}> You don't have enough money!")
        else:
            player.amt -= deposit
            player.bank_date = dt.now()
            player.bank = money + deposit
            cur.execute(f"""
            UPDATE economy
            SET amt = amt - {deposit}, time = '{player.bank_date}', bank = {player.bank}
            WHERE id = '{id}';
            """)
            conn.commit()
            await cmd.send(f"<@!{id}> sent `💲{deposit}` to the bank.")
    elif args[0].lower() == "withdraw":
        try:
            withdraw = int(args[1])
            if withdraw < 0:
                raise ValueError
        except KeyError:
            await cmd.send("Please specify a withdraw amount")
            return
        except ValueError:
            if args[1].lower() == "all":
                withdraw = player.bank
            else:
                await cmd.send("Please check your input again.")
                return
        if withdraw > money:
            await cmd.send(f"<@!{id}> Your bank account doesn't have enough money!")
        else:
            player.amt += withdraw
            player.bank_date = dt.now()
            player.bank = money - withdraw
            cur.execute(f"""
            UPDATE economy
            SET amt = amt + {withdraw}, time = '{player.bank_date}', bank = {player.bank}
            WHERE id = '{id}';
            """)
            conn.commit()
            await cmd.send(f"<@!{id}> withdrew `💲{withdraw}` from the bank.")
