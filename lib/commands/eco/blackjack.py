import asyncio
import discord
import os
import random
from discord.ext import commands
from settings import *


# List of ongoing games and their states
_playing = {}


async def get_bot_hand(cmd, id):
    bot_hand = BlackjackHand([])
    for i in range(2):
        bot_hand.draw()
    while bot_hand.value < 17:
        bot_hand.draw()
    bot_hand.image.save(f"./lib/assets/cards/{id}_bot.png")
    file = discord.File(f"./lib/assets/cards/{id}_bot.png", filename="blackjack.png")
    point, special = bot_hand.get_value()
    em = discord.Embed(
        color = 0x2ECC71,
    )
    footer = f"Current points: {point}"
    if special:
        footer += "*"
    em.set_footer(text=footer)
    em.set_author(name="These are my cards!", icon_url=bot.user.avatar_url)
    em.set_image(url="attachment://blackjack.png")
    await cmd.send(file=file, embed=em)
    os.remove(f"./lib/assets/cards/{id}_bot.png")
    return point


@bot.command(
    name = "blackjack",
    aliases = ["bj"],
    description = "Play blackjack",
    usage = "blackjack <bet amount | default: 0>",
)
@commands.cooldown(1, 15, commands.BucketType.user)
async def _blackjack(cmd, amt = None):
    id = cmd.author.id
    resume = False
    if id in _playing:
        #  The player is currently playing another blackjack
        # game so we must fetch existing data from the cache.
        _playing[id][0] = cmd.message.id
        resume = True
    else:
        #  The player has no ongoing game -> create a new one.
        player = await bot.get_player(id)
        if not player:
            return await cmd.send(f"<@!{id}> To use the economy commands, you must use `{cmd.prefix}daily` first")
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
        await bot.db.conn.execute(
            f"UPDATE economy SET amt = amt - {amt} WHERE id = '{id}';"
        )
        # Write data to cache
        _playing[id] = [cmd.message.id, amt, BlackjackHand([])]
        for i in range(2):
            _playing[id][2].draw()

    if resume:
        await cmd.send("Resuming last game")

    while cmd.message.id == _playing[id][0]:
        point, special = _playing[id][2].get_value()
        footer = f"Current points: {point}"
        if special:
            footer += "*"

        em = discord.Embed(
            title = "Blackjack",
            description = f"Hit {bj[0]} or stay {bj[1]}?",
            color = 0x2ECC71,
        )
        em.set_image(url = "attachment://blackjack.png")
        em.set_author(
            name = f"{cmd.author.name} bet 💲{_playing[id][1]} to play blackjack",
            icon_url = cmd.author.avatar_url,
        )
        em.set_footer(text=footer)

        try:
            await msg.delete()
        except NameError:
            pass

        _playing[id][2].image.save(f"./lib/assets/cards/{id}.png")
        file = discord.File(f"./lib/assets/cards/{id}.png", filename = "blackjack.png")

        msg = await cmd.send(file=file, embed=em)
        os.remove(f"./lib/assets/cards/{id}.png")

        if point > 21:
            del _playing[id]
            bot_point = await get_bot_hand(cmd, id)
            if bot_point > 21:
                return await cmd.send("Both of you lost! 💸")
            else:
                return await cmd.send(f"<@!{cmd.author.id}> lost! 💸")

        for emoji in bj:
            await msg.add_reaction(emoji)
        

        def check(reaction, user):
            return msg.id == reaction.message.id and str(reaction) in bj and user.id == id
        

        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=300.0, check=check)
        except asyncio.TimeoutError:
            if _playing[id][0] == cmd.message.id:
                del _playing[id]
                return await cmd.send(f"<@!{id}> timed out for blackjack game!")
            else:
                return
        else:
            if _playing[id][0] == cmd.message.id:
                choice = bj.index(str(reaction))
                if choice == 0:
                    _playing[id][2].draw()
                else:
                    bot_point = await get_bot_hand(cmd, id)
                    if bot_point > 21 or 21 - bot_point > 21 - point:
                        await bot.db.conn.execute(
                            f"UPDATE economy SET amt = amt + {2 * _playing[id][1]} WHERE id = '{id}';"
                        )
                        await cmd.send(f"<@!{id}> won! 💰")
                    elif 21 - bot_point < 21 - point:
                        await cmd.send(f"<@!{id}> lost! 💸")
                    else:
                        await bot.db.conn.execute(
                            f"UPDATE economy SET amt = amt + {_playing[id][1]} WHERE id = '{id}';"
                        )
                        await cmd.send("Draw!")
                    del _playing[id]
                    return
