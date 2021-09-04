import discord
from discord.ext import commands
from settings import *


@bot.command(
    name = "account",
    aliases = ["acc"],
    description = "View a user's economy account",
    usage = "account <user | default: yourself>",
)
@commands.cooldown(1, 6, commands.BucketType.user)
async def _account(cmd, user: discord.Member = None):
    if user == None:
        user = cmd.author
    if user == bot.user:
        em = discord.Embed(
            title=f"Information about **{user.name}**",
            description=f"**Player** <@!{user.id}>\n**Money** `💲9000000000`\nTotal number of gacha rolls: `-1`",
            color=0x2ECC71,
        )
        await cmd.send(embed=em)
    elif user.bot:
        await cmd.send(f"<@!{user.id}> is a bot user!")
        return
    else:
        id = user.id
        player = await bot.get_player(id)
        if not player:
            return await cmd.send("This user has no account in my database!")
        s = sum(pet.amt for pet in player.pet)
        amt = player.amt
        win = player.win
        total = player.total
        if total == 0:
            rate = "--"
        else:
            rate = 100 * win / total
            rate = "{:.2f}".format(rate)
        em = discord.Embed(
            title=f"Information about {user.name}",
            description=f"**Player** <@!{id}>\n**Money** `💲{amt}`\n**Total number of gacha rolls** `{s}`\n**Battles won** `{win}/{total}` (win rate `{rate}%`)",
            color=0x2ECC71
        )
        em.set_footer(text="This command does not show pet list")
        await cmd.send(embed=em)
