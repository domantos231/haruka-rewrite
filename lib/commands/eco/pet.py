import discord
import math
import asyncio
import gc
from discord.ext import commands
from settings import *


pets_per_page = 9
inline = True


@bot.command(name="pet")
@commands.cooldown(1, 15, commands.BucketType.user)
async def _pet(cmd, user: discord.Member=None):
    if user == None:
        user = cmd.author
    if user == bot.user:
        await cmd.send(embed=discord.Embed(title=f"{user.name}'s pet list",
                description="Currently has 1 pet(s)\n🛸 Lv.`9999` EXP `-1/39996`",
                color=0x2ECC71,))
    elif user.bot:
        await cmd.send(f"<@!{user.id}> is a bot user!")
    else:
        id = str(user.id)
        player = await data(id).player
        if not player:
            return await cmd.send("This user has no data in my database!")
        names = []
        values = []
        for obj in enumerate(player.pet):
            if obj[1].amt > 0:
                pet_id = obj[0]
                obj[1].load()
                names.append(f"{obj[1].img} ID {pet_id}\n[{obj[1].rarity}]")
                values.append(f"Lv.`{obj[1].lv}` EXP `{obj[1].exp}`/`{4 * obj[1].lv}`\nHP `{obj[1].hp_max}` ATK `{obj[1].atk}`")
        pages = 1 + int((len(names)) / pets_per_page)
        em = discord.Embed(title=f"{user.name}'s pet list", description=f"Currently has {len(names)} pet(s)", color=0x2ECC71)
        for i in range(pets_per_page):
            try:
                em.add_field(name=names[i], value=values[i], inline=inline)
            except:
                break
        em.set_footer(text=f"Showing page 1/{pages}")
        msg = await cmd.send(embed=em)
        for emoji in choices[:pages]:
            await msg.add_reaction(emoji)


        def check(reaction, usr):
            return reaction.message.id == msg.id and str(reaction) in choices[:pages] and not usr.bot


        async def react():
            while True:
                done, pending = await asyncio.wait([bot.wait_for("reaction_add", check=check),
                                                    bot.wait_for("reaction_remove", check=check)],
                                                    return_when = asyncio.FIRST_COMPLETED)
                reaction, usr = done.pop().result()
                page = choices.index(str(reaction)) + 1
                em = discord.Embed(title=f"{user.name}'s pet list", description=f"Currently has {len(names)} pet(s)", color=0x2ECC71)
                for i in range(pets_per_page * page - pets_per_page, pets_per_page * page):
                    try:
                        em.add_field(name=names[i], value=values[i], inline=inline)
                    except:
                        break
                em.set_footer(text=f"Showing page {page}/{pages}")
                await msg.edit(embed = em)


        try:
            await asyncio.wait_for(react(), timeout=120.0)
        except asyncio.TimeoutError:
            await msg.clear_reactions()
            del names, values
            gc.collect()
            return


@_pet.error
async def pet_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")
