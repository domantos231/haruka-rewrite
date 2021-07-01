import discord
from discord.ext import commands
from lib.settings import *


@bot.command()
async def get(cmd, arg: int, user: discord.User = None):
    if not await bot.is_owner(cmd.author):
        await cmd.send("This command is available for developers only.")
        return
    if user == None:
        user = cmd.author
    id = str(user.id)
    if user.bot:
        await cmd.send(f"<@!{id}> is a bot user!")
    else:
        null = True
        cur.execute("SELECT id, amt FROM economy;")
        lst = cur.fetchall()
        for data in lst:
            if data[0] == id:
                null = False
                amt = data[1]
                amt += arg
                cur.execute(f"""
                UPDATE economy
                SET amt = {amt}
                WHERE id = '{id}';
                """)
                conn.commit()
                await cmd.send(embed=discord.Embed(title="Request accepted", description="Successfully generated `💲{:.1f}`".format(arg) + f" for <@!{id}>", color=0x2ECC71))
                break
        if null:
            await cmd.send("This user has no data in my database.")


@get.error
async def get_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")