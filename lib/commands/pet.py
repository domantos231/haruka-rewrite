﻿import discord
import math
import asyncio
from discord.ext import commands
from lib.settings import *


@bot.command()
async def pet(cmd, user: discord.Member = None):
    if user == None:
        user = cmd.author
    if user == bot.user:
        await cmd.send(
            embed=discord.Embed(
                title=f"{user.name}'s pet list",
                description="Currently has 1 pet(s)\n🛸 Lv.`9999` EXP `-1/39996`",
                color=0x2ECC71,
            )
        )
    elif user.bot:
        await cmd.send("<@!{0.id}> is a bot user!".format(user))
    else:
        id = str(user.id)
        cur.execute("SELECT * FROM economy;")
        lst = cur.fetchall()
        null = True
        for data in lst:
            if data[0] == id:
                null = False
                name = []
                value = []
                for i in range(5, 57):
                    if data[i] > 0:
                        p = data[i]
                        lv = int((-1 + math.sqrt(1 + 2 * p)) / 2)
                        r = p - 2 * lv * (lv + 1)
                        lv += 1
                        stat = stats(i-5, lv)
                        name.append(f"{petimg[i-5]} ID *{i-5}*")
                        value.append(f"**[{stat.type}]**\nLv. `{lv}` EXP. `{r}/{4*lv}`\nHP `{stat.hp}` ATK `{stat.atk}`")
                pages = 1 + int((len(name)) / 12)
                em = discord.Embed(title=f"{user}'s pet list", description=f"Currently has {len(name)} pet(s)", color=0x2ECC71)
                for i in range(12):
                    try:
                        em.add_field(name=name[i], value=value[i])
                    except:
                        break
                em.set_footer(text=f"Showing page 1/{pages}")
                message = await cmd.send(embed=em)
                for emoji in choices[:pages]:
                    await message.add_reaction(emoji)


                async def delete():
                    await asyncio.sleep(60)
                    await message.edit(embed = discord.Embed(title=f"{cmd.author}'s pet list", description=f"Currently has {len(name)} pet(s)", color=0x2ECC71))
                    await message.clear_reactions()


                def check(reaction, user):
                    return reaction.message == message and str(reaction) in choices and not user.bot


                async def react():
                    while True:
                        done, pending = await asyncio.wait([bot.wait_for("reaction_add", check=check),
                                                            bot.wait_for("reaction_remove", check=check)],
                                                           return_when = asyncio.FIRST_COMPLETED)
                        reaction, user = done.pop().result()
                        if not str(reaction) in choices[:pages]:
                            continue
                        page = choices.index(str(reaction)) + 1
                        em = discord.Embed(title=f"{cmd.author}'s pet list", description=f"Currently has {len(name)} pet(s)", color=0x2ECC71)
                        for i in range(12*page-12, 12*page):
                            try:
                                em.add_field(name=name[i], value=value[i])
                            except:
                                break
                        em.set_footer(text=f"Showing page {page}/{pages}")
                        await message.edit(embed = em)


                await asyncio.wait([delete(), react()], return_when = asyncio.FIRST_COMPLETED)
        if null:
            await cmd.send("This user has no data in my database.")


@pet.error
async def pet_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")