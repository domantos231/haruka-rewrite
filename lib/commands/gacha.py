import discord
from discord.ext import commands
from random import randint
from lib.settings import *


@bot.command()
async def gacha(cmd, n: int = 1):
    if n < 1:
        raise commands.UserInputError
    elif n > 100:
        await cmd.send("The maximum number of rolls you can gacha at a time is 100.")
    else:
        cur.execute("SELECT * FROM economy;")
        lst = cur.fetchall()
        id = str(cmd.author.id)
        for data in lst:
            if data[0] == id:
                if data[1] < n*300:
                    await cmd.send("Not enough money. Gacha costs `💲300`/turn")
                else:
                    amt = data[1]
                    amt -= n*300
                    pet_add = []
                    for i in range(52):
                        pet_add.append(0)
                    for i in range(n):
                        j = randint(1, 1000000) - 1
                        if j < 484848:
                            k = int(j / 30303)
                            pet_add[k] += 1
                        elif j < 848484:
                            k = int(j / 20202) - 8
                            pet_add[k] += 1
                        elif j < 989898:
                            k = int(j / 10101) - 50
                            pet_add[k] += 1
                        elif j < 999999:
                            k = int(j / 3367) - 246
                            pet_add[k] += 1
                        else:
                            pet_add[51] += 1
                    gacha_em = discord.Embed(
                        title=f"Gacha results for {cmd.author}",
                        description=f"Total number of rolls: {n}",
                        color=0x2ECC71,
                    )
                    name = ["COMMON","RARE","EPIC","LEGENDARY","????"]
                    value = ["","","","","",""]
                    add = ""
                    for i in range(52):
                        if pet_add[i] > 0:
                            p = name.index(stats(i, 1).type)
                            value[p] += petimg[i] + f"[{stats(i, 1).type}] +{pet_add[i]}\n"
                            new = data[i+5] + pet_add[i]
                            add += f", pet_{i} = {new}"
                    cur.execute(f"""
                    UPDATE economy
                    SET amt = {amt}{add}
                    WHERE id = '{id}';
                    """)
                    conn.commit()
                    for i in range(5):
                        if len(value[i]) > 0:
                            gacha_em.add_field(name=name[i] + " units", value=value[i], inline=True)
                    await cmd.send(embed=gacha_em)
                break


@gacha.error
async def gacha_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")