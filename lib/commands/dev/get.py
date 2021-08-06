import discord
from discord.ext import commands
from settings import *


@bot.command(name="get")
async def _get(cmd, arg: int, user: discord.User = None):
    if not await bot.is_owner(cmd.author):
        await cmd.send("This command is available for developers only.")
        return
    if user == None:
        user = cmd.author
    id = str(user.id)
    player = data(id).player()
    if user.bot:
        await cmd.send(f"<@!{id}> is a bot user!")
    else:
        try:
            player.amt += arg
            cur.execute(f"""
            UPDATE economy
            SET amt = amt + {arg}
            WHERE id = '{id}';
            """)
            conn.commit()
            await cmd.send(embed=discord.Embed(title="Request accepted", description="Successfully generated `💲{:.1f}`".format(arg) + f" for <@!{id}>", color=0x2ECC71))
        except:
            await cmd.send("This user has no data in my database.")


@_get.error
async def get_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")