import discord
from discord.ext import commands
from lib.settings import *


@bot.command()
async def reset(cmd, user: discord.User = None):
    if await bot.is_owner(cmd.author):
        if user is None:
            cur.execute(f"""
            DELETE FROM economy;
            """)
            conn.commit()
            lst = [300, None, 0, 1.01]
            for i in range(54):
                lst.append(0)
            for id in data.keys():
                data[id] = lst
            await cmd.send(embed=discord.Embed(title="Request accepted", description=f"Successfully removed all from database", color=0x2ECC71))
            return
        id = str(user.id)
        try:
            data[id]
        except:
            await cmd.send("This user has no data in my database!")
        else:
            cur.execute(f"""
            DELETE FROM economy
            WHERE id = '{id}';
            """)
            conn.commit()
            del data[id]
            await cmd.send(embed=discord.Embed(title="Request accepted", description=f"Successfully removed <@!{id}> from database", color=0x2ECC71))
    else:
        await cmd.send("This command is available for developers only.")


@reset.error
async def reset_error(cmd, error):
    if isinstance(error, commands.UserInputError):
        await cmd.send("Please check your input again.")
