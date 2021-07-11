import asyncio
import discord
import math
from random import randint
from threading import Thread
from discord.ext import commands
from lib.settings import *


checker = ["❎", "✅"]


@bot.command()
async def battle(cmd, mem: discord.Member=None):
    if mem == None or mem == cmd.author or mem.bot:
        await cmd.send("Please specify a valid opponent.")
    else:
        em = discord.Embed(title="Battle challenge", description=f"<@!{mem.id}> Do you accept <@!{cmd.author.id}>'s challenge?", color=0x2ECC71)
        em.set_footer(text="This message will expire after 5 minutes")
        message = await cmd.send(embed=em)
        for emoji in checker:
            await message.add_reaction(emoji)


        def check(reaction, user):
            return user == mem and str(reaction) in checker


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
            id_lst = [str(cmd.author.id), str(mem.id)]
            try:
                for id in id_lst:
                    if sum(data[id][4:53]) == 0:
                        raise ValueError
            except:
                await cmd.send("Both players must have at least 1 pet to perform battle.")
                return
            await cmd.send(f"<@!{mem.id}> accepted the challenge.\nChoose at most 3 pets to battle by entering `select <id> <id> <id>`.\nEg. `select 2 43 13`, `select 0 14`")
            pending = [True, True]
            _team = {}
            class Team:
                def __init__(self, user, pet, lv, hp, atk):
                    self.user = user
                    self.pet = pet
                    self.lv = lv
                    self.hp = hp
                    self.atk = atk
                    self.hp_max = hp.copy()


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
                choices = []
                for i in choice:
                    try:
                        i = int(i)
                        if data[id][i + 4] == 0:
                            raise ValueError
                        else:
                            choices.append(i)
                            player_team.append(data[id][i + 4])
                    except:
                        continue
                n = len(player_team)
                _lv = []
                hp = []
                atk = []
                if n == 0 or n > 3:
                    await cmd.send("Please perform a valid selection.")
                    continue
                else:
                    em = discord.Embed(title=f"{message.author} has completed selecting!",
                                       color=0x2ECC71)
                    for i in range(n):
                        pet = petimg[choices[i]]
                        cons = player_team[i]
                        lv = 1 + int((-1 + math.sqrt(1 + 2 * cons)) / 2)
                        stat = stats(choices[i], lv)
                        _lv.append(lv)
                        hp.append(stat.hp)
                        atk.append(stat.atk)
                        em.add_field(name=f"{pet} Lv.`{lv}`", value=f"HP `{stat.hp}` ATK `{stat.atk}`")
                    _team[id] = Team(message.author, choices, _lv, hp, atk)
                    await cmd.send(embed=em)
                    await message.delete()
                    pending[p] = False
            lst = []
            ongoing = True


            def win(attacker_id, target_id):
                cur.execute(f"""
                UPDATE economy
                SET win = win + 1, total = total + 1
                WHERE id = '{attacker_id}';
                """)
                cur.execute(f"""
                UPDATE economy
                SET total = total + 1
                WHERE id = '{target_id}';
                """)
                conn.commit()
                data[attacker_id][56] += 1
                data[attacker_id][57] += 1
                data[target_id][57] += 1


            def proc(rate):
                proc = randint(1, 100000)
                return proc <= 1000 * rate


            turn = 1
            while ongoing:
                for i in range(2):
                    attacker_id = id_lst[i]
                    target_id = id_lst[1 - i]
                    attacker = randint(0, len(_team[attacker_id].pet) - 1)
                    while _team[attacker_id].hp[attacker] == 0:
                        attacker = randint(0, len(_team[attacker_id].pet) - 1)
                    target = randint(0, len(_team[target_id].pet) - 1)
                    while _team[target_id].hp[target] == 0:
                        target = randint(0, len(_team[target_id].pet) - 1)
                    dmg = _team[attacker_id].atk[attacker]
                    if _team[target_id].pet[target] == 0:
                        stat = stats(0, _team[target_id].lv[target])
                        if proc(stat.eff_rate):
                            dmg -= stat.eff_value
                    if _team[target_id].pet[target] == 6:
                        stat = stats(6, _team[target_id].lv[target])
                        dmg += _team[target_id].hp[target] * stat.eff_rate / 100
                        dmg = int(dmg)
                    if dmg < 0:
                        dmg = 0
                    else:
                        _team[target_id].hp[target] -= dmg
                    em = discord.Embed(title="Battle Status", description="Ongoing battle", color=0x2ECC71)
                    if _team[target_id].hp[target] <= 0:
                        _team[target_id].hp[target] = 0
                        if _team[target_id].pet[target] == 5:
                            stat = stats(5, _team[target_id].lv[target])
                            if proc(stat.eff_rate):
                                _team[target_id].hp[target] = stat.eff_value
                        if sum(_team[target_id].hp) == 0:
                            em = discord.Embed(title="Battle Status", description=f"**{_team[id_lst[i]].user.name}** won!", color=0x2ECC71)
                            win(attacker_id, target_id)
                            ongoing = False
                    for k in id_lst:
                        n = len(_team[k].pet)
                        if ongoing:
                            for i in range(n):
                                if _team[k].pet[i] == 1 and _team[k].hp[i] > 0:
                                    stat = stats(1, _team[k].lv[i])
                                    _team[k].hp[i] += stat.eff_value
                                    if _team[k].hp[i] > _team[k].hp_max[i]:
                                        _team[k].hp[i] = _team[k].hp_max[i]
                                if _team[k].pet[i] == 2 and _team[k].hp[i] > 0:
                                    stat = stats(2, _team[k].lv[i])
                                    if proc(stat.eff_rate):
                                        _team[k].hp[i] += stat.eff_value
                                        if _team[k].hp[i] > _team[k].hp_max[i]:
                                            _team[k].hp[i] = _team[k].hp_max[i]
                                if _team[k].pet[i] == 3 and _team[k].hp[i] > 0:
                                    stat = stats(3, _team[k].lv[i])
                                    if proc(stat.eff_rate):
                                        for j in range(n):
                                            _team[k].hp[j] += stat.eff_value
                                            if _team[k].hp[j] > _team[k].hp_max[j]:
                                                _team[k].hp[j] = _team[k].hp_max[j]
                                if _team[k].pet[i] == 4 and _team[k].hp[i] > 0:
                                    stat = stats(4, _team[k].lv[i])
                                    for j in range(n):
                                        _team[k].hp[j] += stat.eff_value
                                        if _team[k].hp[j] > _team[k].hp_max[j]:
                                            _team[k].hp[j] = _team[k].hp_max[j]
                        value = "\n".join(f"`{j+1}`{petimg[_team[k].pet[j]]} Lv.`{_team[k].lv[j]}` HP `{_team[k].hp[j]}/{_team[k].hp_max[j]}` ATK `{_team[k].atk[j]}`" for j in range(n))
                        em.add_field(name=f"{_team[k].user.name}'s team", value=value)
                    em.set_footer(text = f"Turn {turn} - {_team[attacker_id].user.name}")
                    turn += 1
                    lst.append(em)
                    if not ongoing:
                        break
            obj = lst.pop()
            lst.insert(0, obj)
            msg = await cmd.send(embed=lst[0])
            navigate = ["⬅️", "➡️"]
            for emoji in navigate:
                await msg.add_reaction(emoji)


            def check(reaction, user):
                return str(reaction) in navigate and reaction.message.id == msg.id


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


@battle.error
async def battle_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")