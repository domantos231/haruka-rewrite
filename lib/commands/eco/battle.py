import asyncio
import discord
import math
from random import randint
from discord.ext import commands
from settings import *


class NoPet(Exception):
    pass


@bot.command(name="battle")
@commands.cooldown(1, 15, commands.BucketType.user)
async def _battle(cmd, mem: discord.Member=None):
    if mem == None or mem == cmd.author or mem.bot:
        await cmd.send("Please specify a valid opponent.")
    else:
        # Check if both players have pets to battle
        id_lst = [str(cmd.author.id), str(mem.id)]
        name_lst = [cmd.author.name, mem.name]
        try:
            for id in id_lst:
                player = await data(id).player
                if not player:
                    raise NoPet
                if sum(pet.amt for pet in player.pet) == 0:
                    raise NoPet
        except NoPet:
            return await cmd.send("Both players must have at least 1 pet to perform battle.")
        

        # Send battle invite
        em = discord.Embed(title="Battle challenge", description=f"<@!{mem.id}> Do you accept <@!{cmd.author.id}>'s challenge?", color=0x2ECC71)
        em.set_footer(text="This message will expire after 5 minutes")
        message = await cmd.send(embed=em)
        for emoji in checker:
            await message.add_reaction(emoji)


        def check(reaction, user):
            return user.id == mem.id and str(reaction) in checker and reaction.message.id == message.id


        try:
            reaction, user = await bot.wait_for("reaction_add", check = check, timeout = 300.0)
        except asyncio.TimeoutError:
            await message.delete()
            await cmd.send(f"<@!{mem.id}> didn't respond to the battle challenge. Request timed out.")
            return
        await message.delete()
        choice = checker.index(str(reaction))
        if choice == 0:
            await cmd.send(f"<@!{mem.id}> refused to have a duel. What a noob!")
        elif choice == 1:
            await cmd.send(f"<@!{mem.id}> accepted the challenge.\nChoose at most 3 pets to battle by entering `select <id> <id> <id>`.\nEg. `select 2 43 13`, `select 0 14`")
            pending = [True, True]
            team = {}


            def select(message):
                return message.content.lower().startswith("select") and str(message.author.id) in id_lst and message.channel.id == cmd.message.channel.id


            while pending[0] or pending[1]:
                try:
                    message = await bot.wait_for("message", check = select, timeout = 120.0)
                except asyncio.TimeoutError:
                    await cmd.send("Pet selection has timed out. Battle ended.")
                    return
                id = str(message.author.id)
                p = id_lst.index(id)
                if not pending[p]:
                    await cmd.send(f"<@!{message.author.id}>, you have completed selecting!")
                    continue
                choice = message.content.split(" ")[1:]
                player_team = []
                for i in choice:
                    try:
                        i = int(i)
                        player = await data(id).player
                        if player.pet[i].amt == 0:
                            raise ValueError
                        else:
                            player_team.append(player.pet[i])
                    except ValueError:
                        continue
                n = len(player_team)
                if n == 0 or n > 3:
                    await cmd.send("Please perform a valid selection.")
                    continue
                else:
                    team[id] = player_team
                    em = discord.Embed(title=f"{message.author.name} has completed selecting!",
                                       color=0x2ECC71)
                    for pet in team[id]:
                        pet.load()
                        pet.battle_init()
                        em.add_field(
                            name=f"{pet.img} Lv.`{pet.lv}`",
                            value=f"HP `{pet.hp_max}` ATK `{pet.atk}`",
                            inline=True
                        )
                    await cmd.send(embed=em)
                    await message.delete()
                    pending[p] = False


            turn = 1
            ongoing = True
            lst = [] # Embed list for battle status
            while ongoing:
                for i in range(2):
                    attacker_id = id_lst[i]
                    target_id = id_lst[1 - i]
                    attacker = randint(0, len(team[attacker_id]) - 1)
                    while team[attacker_id][attacker].hp == 0:
                        attacker = randint(0, len(team[attacker_id]) - 1)
                    target = randint(0, len(team[target_id]) - 1)
                    while team[target_id][target].hp == 0:
                        target = randint(0, len(team[target_id]) - 1)
                    team[attacker_id][attacker].attack(team[target_id][target])
                    em = discord.Embed(title="Battle Status", description="Ongoing battle", color=0x2ECC71)
                    if sum(pet.hp for pet in team[target_id]) == 0:
                        em = discord.Embed(title="Battle Status", description=f"{name_lst[i]} won!", color=0x2ECC71)
                        await bot.db.conn.execute(f"""
                        UPDATE economy
                        SET win = win + 1, total = total + 1
                        WHERE id = '{attacker_id}';
                        UPDATE economy
                        SET total = total + 1
                        WHERE id = '{target_id}';
                        """)
                        ongoing = False
                    for k in enumerate(id_lst):
                        value = "\n".join(f"`{obj[0] + 1}`{obj[1].img} Lv.`{obj[1].lv}` HP `{obj[1].hp}/{obj[1].hp_max}` ATK `{obj[1].atk}`" for obj in enumerate(team[k[1]]))
                        em.add_field(name=f"{name_lst[k[0]]}'s team", value=value, inline=True)
                    em.set_footer(text = f"Turn {turn} - {name_lst[i]}")
                    turn += 1
                    lst.append(em)
                    if not ongoing:
                        break
            obj = lst.pop()
            lst.insert(0, obj)
            msg = await cmd.send(embed=lst[0])
            for emoji in navigate:
                await msg.add_reaction(emoji)


            def check(reaction, user):
                return str(reaction) in navigate and reaction.message.id == msg.id and not user.bot


            async def view():
                n = 0
                while True:
                    done, pending = await asyncio.wait([bot.wait_for("reaction_add", check=check),
                                                        bot.wait_for("reaction_remove", check=check)],
                                                        return_when = asyncio.FIRST_COMPLETED)
                    reaction, user = done.pop().result()
                    if str(reaction) == "⬅️":
                        if n > 0:
                            n -= 1
                        else:
                            n = len(lst) - 1
                    elif str(reaction) == "➡️":
                        if n == len(lst) - 1:
                            n = 0
                        else:
                            n += 1
                    await msg.edit(embed = lst[n])


            try:
                await asyncio.wait_for(view(), timeout=600.0)
            except asyncio.TimeoutError:
                await msg.edit(embed=lst[0])
                await msg.clear_reactions()
                return


@_battle.error
async def battle_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")
