import discord
import math
from discord.ext import commands
from lib.settings import *


@bot.command()
async def pet(cmd, page: int = 1, user: discord.Member = None):
    if page < 1:
        raise commands.UserInputError
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
        id = user.id
        ecodb = bot.get_channel(int(ECONOMY_ID))
        null = True
        async for message in ecodb.history(limit=200):
            data = message.content.split("/")
            if data[0] == str(id):
                null = False
                name = []
                value = []
                for i in range(6, 58):
                    if int(data[i]) > 0:
                        p = int(data[i])
                        lv = int((-1 + math.sqrt(1 + 2 * p)) / 2)
                        r = p - 2 * lv * (lv + 1)
                        lv += 1
                        stat = stats(i-6, lv)
                        name.append(petimg[i-6])
                        value.append(f"**[{stat.type}]**\nLv. `{lv}` EXP. `{r}/{4*lv}`\nHP `{stat.hp}` ATK `{stat.atk}`")
                pages = 1 + int((len(name)) / 20)
                em = discord.Embed(title=f"{user}'s pet list", description=f"Currently has {len(name)} pet(s)", color=0x2ECC71)
                if page > pages:
                    await cmd.send(f"This pet list only has {pages} page(s) in total!")
                else:
                    for i in range(20*page-20, 20*page):
                        try:
                            em.add_field(name=name[i], value=value[i])
                        except:
                            break
                    em.set_footer(text=f"Showing page {page}/{pages}")
                    await cmd.send(embed=em)
        if null:
            await cmd.send("This user has no data in my database.")


@pet.error
async def pet_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")