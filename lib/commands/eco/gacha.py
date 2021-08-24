import discord
from discord.ext import commands
from random import randint
from settings import *


@bot.command(
    name = "gacha",
    description = "Enjoy the gacha hell.\n-----------------\nRate up details:\n**COMMON** `50%`\n**RARE** `30.33%`\n**EPIC** `15.33%`\n**LEGENDARY** `4.33%`\n**????** `0.01%`",
    usage = "gacha <amount>"
)
@commands.cooldown(1, 20, commands.BucketType.user)
async def _gacha(cmd, n: int = 1):
    if n < 1:
        raise commands.UserInputError
    elif n > 10 and not await bot.is_owner(cmd.author):
        await cmd.send("The maximum number of rolls you can gacha at a time is 10.")
    else:
        id = cmd.author.id
        player = await bot.get_player(id)
        if not player:
            return await cmd.send(f"<@!{id}> To use the economy commands, you must use `{cmd.prefix}daily` first")
        if player.amt < n * 300:
            await cmd.send("Not enough money. Gacha costs `💲300`/turn")
        else:
            player.amt -= n * 300
            pet_add = [0 for i in range(52)]
            for i in range(n):
                j = randint(1, 10000) - 1
                if j < 5000:
                    k = randint(0, 15)
                    pet_add[k] += 1
                elif j < 8033:
                    k = randint(16, 33)
                    pet_add[k] += 1
                elif j < 9566:
                    k = randint(34, 47)
                    pet_add[k] += 1
                elif j < 9999:
                    k = randint(48, 50)
                    pet_add[k] += 1
                else:
                    pet_add[51] += 1
            gacha_em = discord.Embed(
                title=f"Gacha results for {cmd.author.name}",
                description=f"Total number of rolls: {n}",
                color=0x2ECC71,
            )
            display = {}
            sql_query = ""
            for obj in enumerate(pet_add):
                pet_id = obj[0]
                add = obj[1]
                if add > 0:
                    player.pet[pet_id].amt += pet_add[pet_id]
                    if player.pet[pet_id].rarity not in display:
                        display[player.pet[pet_id].rarity] = f"{player.pet[pet_id].img} +{add}"
                    else:
                        display[player.pet[pet_id].rarity] += f", {player.pet[pet_id].img} +{add}"
            await bot.db.conn.execute(
                f"UPDATE economy SET amt = {player.amt}, pet = $1 WHERE id = '{id}';",
                [pet.amt for pet in player.pet]
            )
            for key in display.keys():
                gacha_em.add_field(name=f"{key} units", value=display[key], inline=False)
            await cmd.send(embed=gacha_em)
