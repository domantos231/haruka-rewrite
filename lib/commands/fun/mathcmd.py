import discord
from random import randint
from decimal import Decimal
from settings import *


@bot.command(name="math")
async def _math(cmd):
    type = randint(1, 2)
    if type == 1:
        a = randint(1, 20)
        b = randint(1, 20)
        c = randint(1, 20)
        d = randint(1, 20)
        e = randint(1, 20)
        f = randint(1, 20)
        g = randint(1, 20)
        h = int(b + c * d - e * g + 204)
        m = Decimal((e * f - a) / c)
        ans = randint(1, 6)
        ans_str = ""
        for i in range(1, ans):
            md = Decimal(m + randint(-10, -1))
            ans_str += "\n**" + str(i) + "** {:.2f}".format(md)
        ans_str += "\n**" + str(ans) + "** {:.2f}".format(m)
        for i in range(ans + 1, 7):
            md = Decimal(m + randint(1, 10))
            ans_str += "\n**" + str(i) + "** {:.2f}".format(md)
        message = await cmd.send(
            embed=discord.Embed(
                title="Requested math problem",
                description=f"Given the following equation:\n{a}x + {b} + {c} ( **m**x + {d} ) = {e} ( {f}x + {g} ) + {h}\nWhich of the following values of **m** results in an equation with exactly one solution?" + ans_str,
                color=0x2ECC71,
            )
        )
    if type == 2:
        a = randint(1, 20)
        b = randint(1, 20)
        c = randint(1, 20)
        d = randint(1, 20)
        e = randint(1, 20)
        f = randint(1, 20)
        m = Decimal(-b * e / (a * d))
        ans = randint(1, 6)
        ans_str = ""
        for i in range(1, ans):
            md = Decimal(m + randint(-10, -1))
            ans_str += "\n**" + str(i) + "** {:.2f}".format(md)
        ans_str += "\n**" + str(ans) + "** {:.2f}".format(m)
        for i in range(ans + 1, 7):
            md = Decimal(m + randint(1, 10))
            ans_str += "\n**" + str(i) + "** {:.2f}".format(md)
        message = await cmd.send(
            embed=discord.Embed(
                title="Requested math problem",
                description=f"Given the following system of equations:\n{a}**m**x + {b}y = {c}\n{d}y = {e}x - {f}\nFor which value of **m** is there no (x, y) solutions?" + ans_str,
                color=0x2ECC71,
            )
        )
    for emoji in choices:
        await message.add_reaction(emoji)
    def check(reaction, user):
        return reaction.message.id == message.id and not user.bot
    reaction, user = await bot.wait_for("reaction_add", check=check)
    try:
        choice = 1 + choices.index(str(reaction))
        if choice == ans:
            await cmd.send(f"<@!{user.id}> answered correctly!")
        else:
            await cmd.send(f"<@!{user.id}> answered incorrectly! The correct answer is **{ans}**")
    except:
        await cmd.send(f"The correct answer is **{ans}**")
