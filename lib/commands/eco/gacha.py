import discord
from discord.ext import commands
from random import randint
from settings import *


@bot.command(name="gacha")
@commands.cooldown(1, 15, commands.BucketType.user)
async def _gacha(cmd, n: int = 1):
    if n < 1:
        raise commands.UserInputError
    elif n > 10:
        await cmd.send("The maximum number of rolls you can gacha at a time is 10.")
    else:
        id = str(cmd.author.id)
        player = data(id).player()
        if player.amt < n * 300:
            await cmd.send("Not enough money. Gacha costs `💲300`/turn")
        else:
            player.amt -= n * 300
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
            display = {}
            sql_query = ""
            for obj in enumerate(pet_add):
                pet_id = obj[0]
                add = obj[1]
                if add > 0:
                    sql_query += f", pet[{pet_id}] = pet[{pet_id}] + {add}"
                    if player.pet[pet_id].rarity not in display:
                        display[player.pet[pet_id].rarity] = f"{player.pet[pet_id].img} +{add}"
                    else:
                        display[player.pet[pet_id].rarity] += f", {player.pet[pet_id].img} +{add}"
            cur.execute(f"""
            UPDATE economy
            SET amt = {player.amt}{sql_query}
            WHERE id = '{id}';
            """)
            conn.commit()
            for key in display.keys():
                gacha_em.add_field(name=f"{key} units", value=display[key], inline=False)
            await cmd.send(embed=gacha_em)


@_gacha.error
async def gacha_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")