import discord
from discord.ext import commands
from lib.settings import *


@bot.command(aliases=["acc"])
async def account(cmd, user: discord.Member = None):
    if user == None:
        user = cmd.author
    if user == bot.user:
        em = discord.Embed(
            title="Information about **{0.name}**".format(user),
            description=f"**Player** <@!{user.id}>\n**Money** `💲9000000000`\nTotal number of gacha rolls: `-1`",
            color=0x2ECC71,
        )
        await cmd.send(embed=em)
    elif user.bot:
        await cmd.send(f"<@!{user.id}> is a bot user!")
        return
    else:
        cur.execute("SELECT * FROM economy;")
        lst = cur.fetchall()
        id = str(user.id)
        s = 0
        null = True
        for data in lst:
            if data[0] == str(id):
                null = False
                amt = data[1]
                win = data[57]
                total = data[58]
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
                break
        if null:
            await cmd.send("This user has no data in my database.")


@account.error
async def account_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")
