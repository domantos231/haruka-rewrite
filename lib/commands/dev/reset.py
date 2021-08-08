import discord
from discord.ext import commands
from settings import *


@bot.command(name="reset")
async def _reset(cmd, user: discord.User):
    if await bot.is_owner(cmd.author):
        id = str(user.id)
        if not await data(id).player:
            await cmd.send("This user has no data in my database!")
        else:
            await bot.db.conn.execute(f"""
            DELETE FROM economy
            WHERE id = '{id}';
            """)
            await cmd.send(embed=discord.Embed(title="Request accepted", description=f"Successfully removed <@!{id}> from economy database", color=0x2ECC71))
    else:
        await cmd.send("This command is available for developers only.")


@_reset.error
async def reset_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")
