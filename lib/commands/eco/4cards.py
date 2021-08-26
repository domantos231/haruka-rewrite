import asyncio
import discord
import os
import random
from discord.ext import commands
from settings import *


# List of ongoing games and their states
_playing = {}


@bot.command(
    name = "4cards",
    aliases = ["4c"],
    description = "Play a 4-card game.\nYou are given 4 cards: `A♥️`, `A♦️`, `A♣️`, and `A♠️`. In 2 minutes you have to select 2 cards with the same color.",
    usage = "4cards <bet amount | default: 0>",
)
async def _4cards(cmd, amt = None):
    id = cmd.author.id
    if id not in _playing:
        #  The player has no ongoing game -> create a new one.
        player = await bot.get_player(id)
        if not player:
            return await cmd.send(f"<@!{id}> To use the economy commands, you must use `{cmd.prefix}daily` first")
        _4_cards = ["1a.png", "1b.png", "1c.png", "1d.png"]
        random.shuffle(_4_cards)
        hand = PlayingHand(list(PlayingCard(card, set=True) for card in _4_cards))
        if not amt:
            amt = 0
        try:
            amt = int(amt)
        except ValueError:
            if amt.lower() == "all":
                amt = player.amt
            else:
                raise commands.UserInputError
        if amt < 0:
            raise commands.UserInputError
        if amt > player.amt:
            return await cmd.send("You don't have enough credits!")
        await bot.db.conn.execute(
            f"UPDATE economy SET amt = amt - {amt} WHERE id = '{id}';"
        )
        # Write data to cache
        _playing[id] = [cmd.message.id, amt, hand]
    else:
        return await cmd.send("Please complete your ongoing 4-card game.")
    _playing[id][2].image.save(f"./lib/assets/cards/{id}-4c.png")
    file = discord.File(f"./lib/assets/cards/{id}-4c.png", filename = "4cards.png")
    em = discord.Embed(
        title = "4cards",
        color = 0x2ECC71,
    )
    em.set_author(
        name = f"{cmd.author.name} bet 💲{_playing[id][1]} to play 4cards",
        icon_url = cmd.author.avatar_url,
    )
    em.set_footer(text="Please select a card")
    em.set_image(url = "attachment://4cards.png")
    msg = await cmd.send(file=file, embed=em)
    os.remove(f"./lib/assets/cards/{id}-4c.png")
    for emoji in choices[:4]:
        await msg.add_reaction(emoji)
    

    def check(reaction, user):
        return msg.id == reaction.message.id and user.id == cmd.author.id and str(reaction) in choices[:4]
    

    try:
        reaction, user = await bot.wait_for("reaction_add", check=check, timeout=120.0)
    except asyncio.TimeoutError:
        try:
            if _playing[id][0] == cmd.message.id:
                await cmd.send(f"<@!{id}> timed out for 4-card game and lost `💲{_playing[id][1]}`")
                del _playing[id]
            return
        except KeyError:
            return
    else:
        if cmd.message.id == _playing[id][0]:
            choice = choices.index(str(reaction))
            _playing[id][2].cards[choice].set = False
            _playing[id][2].image.save(f"./lib/assets/cards/{id}-4c.png")
            file = discord.File(f"./lib/assets/cards/{id}-4c.png", filename = "4cards.png")
            em = discord.Embed(
                title = "4cards",
                color = 0x2ECC71,
            )
            em.set_author(
                name = f"{cmd.author.name} bet 💲{_playing[id][1]} to play 4cards",
                icon_url = cmd.author.avatar_url,
            )
            em.set_footer(text="Please select another card")
            em.set_image(url = "attachment://4cards.png")
            try:
                await msg.delete()
            except:
                pass
            msg = await cmd.send(file=file, embed=em)
            os.remove(f"./lib/assets/cards/{id}-4c.png")
            for emoji in choices[:4]:
                await msg.add_reaction(emoji)


            def check(reaction, user):
                if str(reaction) in choices[:4]:
                    choice = choices.index(str(reaction))
                    return msg.id == reaction.message.id and user.id == cmd.author.id and _playing[id][2].cards[choice].set
                return False
                        

            try:
                reaction, user = await bot.wait_for("reaction_add", check=check, timeout=120.0)
            except asyncio.TimeoutError:
                try:
                    if _playing[id][0] == cmd.message.id:
                        await cmd.send(f"<@!{id}> timed out for 4-card game and lost `💲{_playing[id][1]}`")
                        del _playing[id]
                    return
                except KeyError:
                    return
            else:
                if cmd.message.id == _playing[id][0]:
                    choice = choices.index(str(reaction))
                    _playing[id][2].cards[choice].set = False
                    _playing[id][2].image.save(f"./lib/assets/cards/{id}-4c.png")
                    file = discord.File(f"./lib/assets/cards/{id}-4c.png", filename = "4cards.png")
                    file = discord.File(f"./lib/assets/cards/{id}-4c.png", filename = "4cards.png")
                    em = discord.Embed(
                        title = "4cards",
                        color = 0x2ECC71,
                    )
                    em.set_author(
                        name = f"{cmd.author.name} bet 💲{_playing[id][1]} to play 4cards",
                        icon_url = cmd.author.avatar_url,
                    )
                    suits = []
                    for card in _playing[id][2].cards:
                        if card.set:
                            suits.append(card.suit)
                    suits.sort()
                    if suits == [0, 1] or suits == [2, 3]:
                        em.set_footer(text=f"{cmd.author.name} won 💲{_playing[id][1]}!")
                        await bot.db.conn.execute(
                            f"UPDATE economy SET amt = amt + {2 * _playing[id][1]} WHERE id = '{id}';"
                        )
                    else:
                        em.set_footer(text=f"{cmd.author.name} lost 💲{_playing[id][1]}!")
                    em.set_image(url = "attachment://4cards.png")
                    try:
                        await msg.delete()
                    except:
                        pass
                    msg = await cmd.send(file=file, embed=em)
                    os.remove(f"./lib/assets/cards/{id}-4c.png")
                    del _playing[id]
                    return
                else:
                    return
        else:
            return
